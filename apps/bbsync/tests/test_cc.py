import json

import pytest

from apps.bbsync.cc import CCBuilder
from apps.bbsync.tests.factories import BugzillaComponentFactory, BugzillaProductFactory
from osidb.models import Affect, Flaw
from osidb.tests.factories import (
    AffectFactory,
    FlawFactory,
    PsModuleFactory,
    PsProductFactory,
    PsUpdateStreamFactory,
)

pytestmark = pytest.mark.unit


class TestCCBuilder:
    def prepare_flaw(
        self,
        affects=None,
        embargoed=False,
        old_affects=None,
        old_cc=None,
    ):
        """
        helper to initialize flaw with affects
        provided only abbreviated definitions
        """

        def prepare_affect(affect):
            """
            helper to initialize affect
            """
            if isinstance(affect, tuple):
                return {
                    "ps_module": affect[0],
                    "ps_component": affect[1],
                    "affectedness": affect[2]
                    if len(affect) > 2
                    else Affect.AffectAffectedness.AFFECTED,
                    "resolution": affect[3]
                    if len(affect) > 3
                    else Affect.AffectResolution.FIX,
                }
            else:
                return affect

        affects = (
            [] if affects is None else [prepare_affect(affect) for affect in affects]
        )
        old_affects = (
            []
            if old_affects is None
            else [prepare_affect(affect) for affect in old_affects]
        )

        meta_attr = {}
        if old_cc is not None:
            meta_attr["cc"] = '["' + '", "'.join(old_cc) + '"]'
        if old_affects is not None:
            meta_attr["original_srtnotes"] = (
                '{"affects": ' + json.dumps(old_affects) + "}"
            )

        flaw = FlawFactory(
            embargoed=embargoed,
            meta_attr=meta_attr,
        )
        for affect in affects:
            AffectFactory(flaw=flaw, **affect)

        return flaw

    def test_prepare(self):
        self.prepare_flaw(
            affects=[
                ("rhel-6", "kernel"),
                ("rhel-7", "openssl"),
            ],
            old_affects=[
                ("rhel-6", "kernel"),
            ],
            old_cc=[
                "email@redhat.com",
                "someone@gmail.com",
            ],
        )
        flaw = Flaw.objects.first()
        assert flaw
        assert flaw.embargoed == False
        assert flaw.meta_attr["cc"] == '["email@redhat.com", "someone@gmail.com"]'
        assert (
            flaw.meta_attr["original_srtnotes"]
            == '{"affects": [{"ps_module": "rhel-6", "ps_component": "kernel", "affectedness": "AFFECTED", "resolution": "FIX"}]}'
        )
        assert flaw.affects.count() == 2
        assert flaw.affects.filter(ps_module="rhel-6", ps_component="kernel").exists()
        assert flaw.affects.filter(ps_module="rhel-7", ps_component="openssl").exists()

    ###############
    # FLAW CREATE #
    ###############

    def test_empty(self):
        """
        test that no affects result in empty CCs
        """
        flaw = FlawFactory()

        cc_builder = CCBuilder(flaw)
        add_cc, remove_cc = cc_builder.content
        assert not add_cc
        assert not remove_cc

    def test_unknown(self):
        """
        test that affect with an unknown PS module results in empty CCs
        """
        flaw = FlawFactory()
        AffectFactory(
            flaw=flaw,
            affectedness=Affect.AffectAffectedness.AFFECTED,
            resolution=Affect.AffectResolution.FIX,
        )

        cc_builder = CCBuilder(flaw)
        add_cc, remove_cc = cc_builder.content
        assert not add_cc
        assert not remove_cc

    def test_community(self):
        """
        test that community affect results in empty CCs
        """
        flaw = FlawFactory()
        affect = AffectFactory(
            flaw=flaw,
            affectedness=Affect.AffectAffectedness.AFFECTED,
            resolution=Affect.AffectResolution.FIX,
        )
        ps_product = PsProductFactory(business_unit="Community")
        PsModuleFactory(
            name=affect.ps_module,
            default_cc=["me@redhat.com"],
            ps_product=ps_product,
        )

        cc_builder = CCBuilder(flaw)
        add_cc, remove_cc = cc_builder.content
        assert not add_cc
        assert not remove_cc

    @pytest.mark.parametrize(
        "cc,embargoed",
        [
            ([], True),
            (["me@redhat.com", "you@redhat.com"], False),
        ],
    )
    def test_notaffected(self, cc, embargoed):
        """
        test that notaffected affects result in empty CCs
        however this restriction only applies to embargoed flaws
        """
        flaw = FlawFactory(embargoed=embargoed)
        affect1 = AffectFactory(
            flaw=flaw, affectedness=Affect.AffectAffectedness.NOTAFFECTED
        )
        affect2 = AffectFactory(
            flaw=flaw,
            affectedness=Affect.AffectAffectedness.AFFECTED,
            resolution=Affect.AffectResolution.WONTFIX,
        )
        PsModuleFactory(
            name=affect1.ps_module,
            default_cc=["me@redhat.com"],
        )
        PsModuleFactory(
            name=affect2.ps_module,
            default_cc=["you@redhat.com"],
        )

        cc_builder = CCBuilder(flaw)
        add_cc, remove_cc = cc_builder.content
        assert add_cc == cc
        assert not remove_cc

    @pytest.mark.parametrize(
        "cc,private_trackers_allowed",
        [
            (["me@redhat.com", "you@redhat.com"], True),
            ([], False),
        ],
    )
    def test_private_trackers_allowed(self, cc, private_trackers_allowed):
        """
        test that the CCs are empty if embargoed
        when private trackers are not allowed
        """
        flaw = FlawFactory(embargoed=True)
        affect = AffectFactory(
            flaw=flaw,
            affectedness=Affect.AffectAffectedness.AFFECTED,
            resolution=Affect.AffectResolution.FIX,
        )
        PsModuleFactory(
            name=affect.ps_module,
            default_cc=["me@redhat.com"],
            private_tracker_cc=["you@redhat.com"],
            private_trackers_allowed=private_trackers_allowed,
        )

        cc_builder = CCBuilder(flaw)
        add_cc, remove_cc = cc_builder.content
        assert add_cc == cc
        assert not remove_cc

        # self.prepare_flaw(
        #     affects=[
        #         ("rhel-6", "kernel"),
        #         ("rhel-7", "openssl"),
        #     ],
        #     old_affects=[
        #         ("rhel-6", "kernel"),
        #     ],
        #     old_cc=[
        #         "email@redhat.com",
        #         "someone@gmail.com",
        #     ],

    # TODO RHSCL

    ###############
    # FLAW UPDATE #
    ###############
