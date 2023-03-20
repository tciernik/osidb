"""
    tests of Jira Task Manager service (Taskman)

    This class uses VCR in order to not call real Jira endpoints
    during regular tests, and it is recommendend to use Stage Jira instance for
    generating new cassettes, that will requires configuring .env file
    with at least the following ENVs:
    * JIRA_TASKMAN_URL
    * JIRA_TASKMAN_TOKEN
    * JIRA_TASKMAN_PROJECT_KEY
    * HTTPS_PROXY (only required if using Red Hat's stage Jira)
"""

import pytest
import vcr

from apps.taskman.service import JiraTaskmanQuerier, TaskStatus
from osidb.tests.factories import AffectFactory, FlawFactory

my_vcr = vcr.VCR(
    record_mode="once",
    match_on=["uri", "method"],
)


class TestTaskmanService(object):
    @pytest.mark.vcr
    def test_create_or_update_task(self):
        """
        Test that service is able to create, get and sync a task from Jira
        """
        # Remove randomness to reuse VCR every possible time
        flaw = FlawFactory(embargoed=False, uuid="9d9b3b14-0c44-4030-883c-8610f7e2879b")
        AffectFactory(flaw=flaw)

        response1 = JiraTaskmanQuerier().create_or_update_task(
            flaw=flaw, fail_if_exists=True
        )
        assert response1.status_code == 201
        assert response1.data["fields"]["summary"] == flaw.title

        response2 = JiraTaskmanQuerier().get_task(response1.data["id"])
        assert response2.status_code == 200

        response3 = JiraTaskmanQuerier().get_task(response1.data["key"])
        assert response3.status_code == 200

        response4 = JiraTaskmanQuerier().get_task_by_flaw(flaw.uuid)
        assert response4.status_code == 200

        response5 = JiraTaskmanQuerier().get_task("ERRORKEY123")
        assert response5.status_code == 404

        old_title = flaw.title
        new_title = f"{old_title} edited title"

        flaw.title = new_title
        flaw.save()

        response6 = JiraTaskmanQuerier().create_or_update_task(
            flaw=flaw, fail_if_exists=True
        )
        assert response6.status_code == 409
        assert response6.data["existing_task"]["fields"]["summary"] == old_title

        response7 = JiraTaskmanQuerier().create_or_update_task(
            flaw=flaw, fail_if_exists=False
        )
        assert response7.status_code == 204

        response8 = JiraTaskmanQuerier().get_task_by_flaw(flaw.uuid)
        assert response8.data["fields"]["summary"] == new_title

    @pytest.mark.vcr
    def test_update_task_status(self):
        """
        Test that service is able to update task workflow status from Jira
        """
        # Remove randomness to reuse VCR every possible time
        flaw = FlawFactory(embargoed=False, uuid="4823d62a-a59f-49f4-8d79-be9f7d792dfa")

        response1 = JiraTaskmanQuerier().create_or_update_task(flaw=flaw)
        assert response1.status_code == 204

        response2 = JiraTaskmanQuerier().get_task_by_flaw(flaw.uuid)

        response3 = JiraTaskmanQuerier().update_task_status(
            response2.data["key"], TaskStatus.CLOSED
        )
        assert response3.status_code == 200

        response4 = JiraTaskmanQuerier().get_task(response2.data["key"])
        assert response4.status_code == 200
        assert response4.data["fields"]["status"]["name"] == TaskStatus.CLOSED

    @pytest.mark.vcr
    def test_comments(self):
        """
        Test that service is able to create and update a comment from Jira
        """
        # Remove randomness to reuse VCR every possible time
        flaw = FlawFactory(embargoed=False, uuid="99cce9ba-829d-4933-b4c1-44533d819e77")

        response1 = JiraTaskmanQuerier().create_or_update_task(flaw=flaw)
        assert response1.status_code == 201

        response2 = JiraTaskmanQuerier().create_comment(
            response1.data["key"], "user@redhat.com", "New comment"
        )
        assert response2.status_code == 201

        response3 = JiraTaskmanQuerier().update_comment(
            response1.data["key"],
            response2.data["id"],
            "user@redhat.com",
            "Edited comment",
        )
        assert response3.status_code == 200

    @pytest.mark.vcr
    def test_groups(self):
        """
        Test that service is able to create and update a group (epic) from Jira
        """
        # Remove randomness to reuse VCR every possible time
        flaw1 = FlawFactory(
            embargoed=False, uuid="f49b20b2-b9ba-47d7-bf17-b7685f484f51"
        )
        response1 = JiraTaskmanQuerier().create_or_update_task(flaw=flaw1)
        assert response1.status_code == 201

        flaw2 = FlawFactory(
            embargoed=False, uuid="8c502e80-768d-4534-bb02-4db747611319"
        )
        response2 = JiraTaskmanQuerier().create_or_update_task(flaw=flaw2)
        assert response2.status_code == 201

        response3 = JiraTaskmanQuerier().create_group(
            name="curl issues group", description="group for issues related to curl lib"
        )
        assert response3.status_code == 201

        response4 = JiraTaskmanQuerier().add_task_into_group(
            issue_key=response1.data["key"], group_key=response3.data["key"]
        )
        assert response4.status_code == 200

        response5 = JiraTaskmanQuerier().add_task_into_group(
            issue_key=response2.data["key"], group_key=response3.data["key"]
        )
        assert response5.status_code == 200

        response6 = JiraTaskmanQuerier().search_task_by_group(response3.data["key"])
        assert len(response6.data) == 2
