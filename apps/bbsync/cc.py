import json
import logging
import re
from typing import List, Optional, Tuple

from osidb.models import Affect, Flaw, PsContact, PsModule, PsUpdateStream

from .constants import RHSCL_BTS_KEY, USER_BLACKLIST
from .exceptions import ProductDataError
from .models import BugzillaComponent

logger = logging.getLogger(__name__)


class AffectCCBuilder:
    """
    affect CC list builder
    """

    def __init__(self, affect: Affect, embargoed: bool) -> None:
        """
        init stuff
        expects a valid affect
        """
        self.affect = affect
        self.ps_module = affect.ps_module
        self.ps_component = affect.ps_component
        self.ps_module_obj = PsModule.objects.get(name=affect.ps_module)
        self.embargoed = embargoed

        self.bz_component = self.ps2bz_component() if self.is_bugzilla else None

    @property
    def is_bugzilla(self) -> bool:
        """
        check that this PS module is tracked in Bugzilla
        """
        return self.ps_module_obj.bts_name == "bugzilla"

    def ps2bz_component(self) -> str:
        """
        translate PS component to Bugzilla one

        there are three posible options how to map to the Bugzilla component
        component overrides | component split-off | identity
        """
        if (
            self.ps_module_obj.component_overrides
            and self.ps_component in self.ps_module_obj.component_overrides
        ):
            override = self.ps_module_obj.component_overrides[self.ps_component]
            if override is not None:
                return override["component"] if isinstance(override, dict) else override

        elif "/" in self.ps_component:
            return self.ps_component.split("/")[-1]

        return self.ps_component

    @property
    def cc(self) -> List[str]:
        """
        CC list getter
        """
        # skip modules with private trackers not allowed if embargoed
        if self.embargoed and not self.ps_module_obj.private_trackers_allowed:
            return []

        cc_list = self.module_cc() + self.component_cc() + self.bugzilla_cc()

        cc_list = [self.expand_alias(cc) for cc in cc_list]
        cc_list = [self.append_domain(cc) for cc in cc_list]

        if self.embargoed:
            cc_list = [
                cc
                for cc in cc_list
                if not self.is_blacklisted(cc) and self.is_redhat(cc)
            ]

        return cc_list

    def append_domain(self, cc: str) -> str:
        """
        append @redhat.com domain
        in case no domain is present
        """
        return cc if "@" in cc else f"{cc}@redhat.com"

    def expand_alias(self, cc: str) -> str:
        """
        expand an alias to the actual email
        in the case this is actually an alias
        """
        contact = PsContact.objects.filter(username=cc).first()
        if not contact:
            return cc

        if self.ps_module_obj.bts_name == "bugzilla":
            return contact.bz_username

        elif self.ps_module_obj.bts_name == "jboss":
            return contact.jboss_username

        else:
            raise ProductDataError(f"Unknown BTS name {self.ps_module_obj.bts_name}")

    def is_blacklisted(self, cc: str) -> bool:
        """
        check and return whether the CC is on the blacklist
        """
        return cc in USER_BLACKLIST

    def is_redhat(self, cc: str) -> bool:
        """
        check and return whether the CC is RH one
        """
        return cc.endswith("@redhat.com")

    def component_cc(self) -> List[str]:
        """
        generate CCs based on component
        """
        # exact match
        if self.bz_component in self.ps_module_obj.component_cc:
            return self.ps_module_obj.component_cc.get(self.bz_component, [])

        cc_list = []
        # wildcard match
        for component_pattern, component_cc in self.ps_module_obj.component_cc.items():
            if "*" in component_pattern:
                re_pattern = re.escape(component_pattern).replace("\\*", ".+")
                if re.match(re_pattern, self.bz_component):
                    cc_list.update(component_cc)

        return cc_list

    def module_cc(self) -> List[str]:
        """
        generate CCs based on module
        """
        cc_list = []

        # default CCs
        if self.ps_module_obj.default_cc:
            cc_list.extend(self.ps_module_obj.default_cc)

        # extra CCs if embargoed
        if self.embargoed and self.ps_module_obj.private_tracker_cc:
            cc_list.extend(self.ps_module_obj.private_tracker_cc)

        return cc_list

    def bugzilla_cc(self) -> List[str]:
        """
        generate CCs based on Bugzilla product and component
        """
        if not self.is_bugzilla:
            return []

        bz_component_obj = BugzillaComponent.objects.filter(
            product__name=self.ps_module_obj.bts_key, component_name=self.bz_component
        ).first()

        if not bz_component_obj:
            return []

        cc_list = []
        if bz_component_obj.default_cc:
            cc_list.update(bz_component_obj.default_cc)
        if bz_component_obj.default_owner:
            cc_list.add(bz_component_obj.default_owner)

        return cc_list


class RHSCLAffectCCBuilder(AffectCCBuilder):
    """
    Red Hat Software Collections affect CC list builder
    introduces special differences from the base class
    """

    def collections(self) -> List[str]:
        """
        generate collections for the PS module
        """
        collections = set()
        for stream in PsUpdateStream.objects.filter(ps_module__name=self.ps_module):
            collections = collections.union(stream.collections)

        return list(collections)

    def collection_component(self) -> Tuple[Optional[str], str]:
        """
        parse RHSCL PS component into collection and
        Bugzilla component and return them as a tuple
        """
        matched_collections = [
            collection
            for collection in self.collections()
            if self.ps_component.startswith(collection + "-")
            or self.ps_component == collection
        ]

        if not matched_collections:
            return None, self.ps_component

        if len(matched_collections) > 1:
            raise ProductDataError(
                f"Components' {self.ps_component} prefix matches more than "
                f"one valid collection: {', '.join(matched_collections)}"
            )

        collection = matched_collections[0]
        if collection and self.ps_component != collection:
            return collection, self.ps_component[len(collection) + 1 :]

        return collection, self.ps_component

    def ps2bz_component(self) -> str:
        """
        translate PS component to Bugzilla one
        RH software collections special case
        """
        try:
            collection, bz_component = self.collection_component()
        except ProductDataError:
            # ignore exception when component matches more than one RHSCL
            # collection and just use the previous component instead
            return self.ps_component

        # additionally store collection
        # which may be potentially None
        self.collection = collection

        return bz_component

    def component_cc(self) -> List[str]:
        """
        generate CCs based on component
        RH software collections special case
        """
        cc_list = self.ps_module_obj.component_cc.get(self.bz_component, [])
        cc_list.update(
            self.ps_module_obj.component_cc.get(self.collection, [])
            if self.collection
            else []
        )

        return cc_list


class CCBuilder:
    """
    Bugzilla flaw CC list array builder
    """

    def __init__(self, flaw: Flaw, old_flaw: Optional[Flaw] = None) -> None:
        """
        init stuff
        parametr old_flaw is optional as there is no old flaw on creation
        and if not set we consider the query to be a create query
        """
        self.flaw = flaw
        self.old_flaw = old_flaw

        # unless the flaw is being created
        # we extract the previous data
        if not old_flaw:
            return

        self.old_cc = json.loads(self.old_flaw.meta_attr.get("cc", "[]"))

        srtnotes = json.loads(self.old_flaw.meta_attr.get("original_srtnotes", "{}"))
        old_affects = [
            (affect["ps_module"], affect["ps_component"])
            for affect in srtnotes.get("affects", [])
        ]
        self.added_affects = [
            affect
            for affect in self.flaw.affects.all()
            if (affect.ps_module, affect.ps_component) not in old_affects
        ]

    @property
    def content(self) -> Tuple[List[str], List[str]]:
        """
        content getter shorcut
        sort result to easy compare
        """
        add_cc, remove_cc = self.generate()
        return sorted(add_cc), sorted(remove_cc)

    def generate(self) -> Tuple[List[str], List[str]]:
        """
        generate content
        """
        all_cc = self.affect_list2cc(self.flaw.affects.all())

        if not self.old_flaw:
            # on create we add all
            # and remove nothing
            add_cc = all_cc
            remove_cc = []

        elif self.old_flaw.embargoed and not self.flaw.embargoed:
            # on unembargo we add and remove all
            add_cc = all_cc
            remove_cc = list(set(self.old_cc) - set(all_cc))

        else:
            # on update we only add the CCs from new affects
            # so we do not re-add people who removed themselves
            # and remove whatever is not needed any more
            add_cc = self.affect_list2cc(self.added_affects)
            remove_cc = list(set(self.old_cc) - set(all_cc))

        return add_cc, remove_cc

    def affect_list2cc(self, affects: List[Affect]) -> List[str]:
        """
        process the list of affects and return the corresponding list of CCs
        """
        cc_list = set()

        for affect in affects:
            # exclude unknown PS modules
            if self.is_unknown(affect):
                logger.error(
                    f"Affect {affect.uuid} contains unknown PS module: {affect.ps_module}"
                )
                continue

            # exclude community products
            # which was requested to reduce the spam to the communities
            if self.is_community(affect):
                continue

            # for some reason in SFM2 we ignore affects set as not affected or not to be fixed
            # only for embargoed flaws so to keep the functional parity we continue with it
            if self.flaw.embargoed and self.is_notaffected(affect):
                continue

            cc_list.update(self.affect2cc(affect))

        return list(cc_list)

    def affect2cc(self, affect: Affect) -> List[str]:
        """
        process an affect and return the corresponding list of CCs
        """
        affect_cc_builder_class = (
            RHSCLAffectCCBuilder if self.is_rhscl(affect) else AffectCCBuilder
        )
        affect_cc_builder = affect_cc_builder_class(affect, self.flaw.embargoed)
        return affect_cc_builder.cc

    def is_community(self, affect: Affect) -> bool:
        """
        check and return whether the given affect is community one
        """
        return PsModule.objects.filter(
            name=affect.ps_module, ps_product__business_unit="Community"
        ).exists()

    def is_notaffected(self, affect: Affect) -> bool:
        """
        check and return whether the given affect is set as not affected or not to be fixed
        """
        return (
            affect.affectedness == Affect.AffectFix.NOTAFFECTED
            or affect.resolution == Affect.AffectResolution.WONTFIX
        )

    def is_rhscl(self, affect: Affect) -> bool:
        """
        check and return whether the given affect is RHSCL one
        """
        return PsModule.objects.filter(
            name=affect.ps_module, bts_key=RHSCL_BTS_KEY
        ).exists()

    def is_unknown(self, affect: Affect) -> bool:
        """
        check and return whether the given affect has unknown PS module
        """
        return not PsModule.objects.filter(name=affect.ps_module).exists()
