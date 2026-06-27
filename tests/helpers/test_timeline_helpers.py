"""Live integration tests for Timeline helpers — sequential upsert workflow.

Tests run in strict order against staging using TEST_JOB_DISPLAY_ID2 (4000000).
The sequence exercises: delete all -> create -> upsert -> stale-write rejection
-> full lifecycle through all 9 helpers -> final state verification.

Requires valid staging credentials in environment or ``.env.staging``.
"""

import pytest

from ab.api.models.jobs import (
    InTheFieldTaskRequest,
    TimelineSaveResponse,
)
from ab.exceptions import RequestError
from tests.constants import (
    TEST_JOB_DISPLAY_ID2,
    TEST_PK_END_DATE,
    TEST_PK_START_DATE,
    TEST_PU_END_DATE,
    TEST_PU_START_DATE,
    TEST_ST_END_DATE,
    TEST_ST_START_DATE,
    TEST_TR_DELIVERY_COMPLETED_DATE,
    TEST_TR_PICKUP_COMPLETED_DATE,
    TEST_TR_SCHEDULED_DATE,
)

pytestmark = pytest.mark.live

JOB = TEST_JOB_DISPLAY_ID2


class TestTimelineHelperSequence:
    """Sequential timeline helper tests — each builds on prior state."""

    def test_step_00_delete_all(self, api):
        """Clean slate: delete all timeline tasks for the test job."""
        api.jobs.tasks.delete_all(JOB)

        # Verify all tasks are gone
        for code in ["PU", "PK", "ST", "CP"]:
            _, task = api.jobs.tasks.get_task(JOB, code)
            assert task is None, f"Task {code} should not exist after delete_all"

    def test_step_01_pack_start(self, api):
        """Create PK task with pack_start — first task on clean job."""
        resp = api.jobs.tasks.pack_start(JOB, start=TEST_PK_START_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        # Verify task was created with correct start date
        _, task = api.jobs.tasks.get_task(JOB, "PK")
        assert task is not None, "PK task should exist after pack_start"
        time_log = task.get("timeLog") or {}
        assert time_log.get("start") is not None, "PK timeLog.start should be set"

    def test_step_02_schedule(self, api):
        """Schedule PU task — proceeds despite status > 2 (logs warning)."""
        resp = api.jobs.tasks.schedule(JOB, start=TEST_PU_START_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        # Verify PU task has planned start date
        _, task = api.jobs.tasks.get_task(JOB, "PU")
        assert task is not None, "PU task should exist after schedule"
        assert task.get("plannedStartDate") is not None, "PU plannedStartDate should be set"

    def test_step_03_received_stale_fails(self, api):
        """Stale write: POST PU update WITHOUT id/modifiedDate — expect failure.

        Bypasses the helper's auto-fetch by calling set_task() directly with
        a model that lacks the server's id and modifiedDate. The server should
        reject this because the task already exists (HTTP 409).
        """
        model = InTheFieldTaskRequest(
            task_code="PU",
            completed_date=TEST_PU_END_DATE,
        )
        # Deliberately do NOT enrich with id/modifiedDate
        with pytest.raises(RequestError) as exc_info:
            api.jobs.tasks.set_task(JOB, "PU", model)
        assert exc_info.value.status_code == 409, (
            f"Expected HTTP 409 for stale write, got {exc_info.value.status_code}"
        )

    def test_step_04_received_fresh_succeeds(self, api):
        """Fresh write: received() auto-fetches id/modifiedDate — succeeds."""
        resp = api.jobs.tasks.received(JOB, end=TEST_PU_END_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        # Verify PU task now has completed date AND preserved plannedStartDate
        _, task = api.jobs.tasks.get_task(JOB, "PU")
        assert task is not None
        assert task.get("completedDate") is not None, "PU completedDate should be set"
        assert task.get("plannedStartDate") is not None, (
            "PU plannedStartDate should be preserved from schedule()"
        )

    def test_step_05_pack_finish(self, api):
        """Pack finish — upserts existing PK task with end time."""
        resp = api.jobs.tasks.pack_finish(JOB, end=TEST_PK_END_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        # Verify PK task has both start and end
        _, task = api.jobs.tasks.get_task(JOB, "PK")
        assert task is not None
        time_log = task.get("timeLog") or {}
        assert time_log.get("start") is not None, "PK timeLog.start should be preserved"
        assert time_log.get("end") is not None, "PK timeLog.end should be set"

    def test_step_06_storage_begin(self, api):
        """Storage begin — creates ST task with start time."""
        resp = api.jobs.tasks.storage_begin(JOB, start=TEST_ST_START_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        _, task = api.jobs.tasks.get_task(JOB, "ST")
        assert task is not None
        time_log = task.get("timeLog") or {}
        assert time_log.get("start") is not None, "ST timeLog.start should be set"

    def test_step_07_storage_end(self, api):
        """Storage end — upserts existing ST task with end time."""
        resp = api.jobs.tasks.storage_end(JOB, end=TEST_ST_END_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        _, task = api.jobs.tasks.get_task(JOB, "ST")
        assert task is not None
        time_log = task.get("timeLog") or {}
        assert time_log.get("start") is not None, "ST timeLog.start should be preserved"
        assert time_log.get("end") is not None, "ST timeLog.end should be set"

    def test_step_08_carrier_schedule(self, api):
        """Carrier schedule — creates CP task with scheduled date."""
        resp = api.jobs.tasks.carrier_schedule(JOB, start=TEST_TR_SCHEDULED_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        _, task = api.jobs.tasks.get_task(JOB, "CP")
        assert task is not None
        assert task.get("scheduledDate") is not None, "CP scheduledDate should be set"

    def test_step_09_carrier_pickup(self, api):
        """Carrier pickup — upserts existing CP task, preserves scheduledDate."""
        resp = api.jobs.tasks.carrier_pickup(JOB, start=TEST_TR_PICKUP_COMPLETED_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        _, task = api.jobs.tasks.get_task(JOB, "CP")
        assert task is not None
        assert task.get("pickupCompletedDate") is not None, "CP pickupCompletedDate should be set"
        assert task.get("scheduledDate") is not None, (
            "CP scheduledDate should be preserved from carrier_schedule()"
        )

    def test_step_10_carrier_delivery(self, api):
        """Carrier delivery — upserts existing CP task, preserves prior dates."""
        resp = api.jobs.tasks.carrier_delivery(JOB, end=TEST_TR_DELIVERY_COMPLETED_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        _, task = api.jobs.tasks.get_task(JOB, "CP")
        assert task is not None
        assert task.get("deliveryCompletedDate") is not None, "CP deliveryCompletedDate should be set"
        assert task.get("scheduledDate") is not None, (
            "CP scheduledDate should be preserved"
        )
        assert task.get("pickupCompletedDate") is not None, (
            "CP pickupCompletedDate should be preserved"
        )

    def test_step_11_verify_final_state(self, api):
        """Verify all 4 task types have expected dates after full sequence."""
        # PU task — received() should preserve plannedStartDate from schedule()
        _, pu = api.jobs.tasks.get_task(JOB, "PU")
        assert pu is not None, "PU task should exist"
        assert pu.get("completedDate") is not None, "PU completedDate"
        assert pu.get("plannedStartDate") is not None, "PU plannedStartDate preserved"

        # PK task — should have timeLog with start and end
        _, pk = api.jobs.tasks.get_task(JOB, "PK")
        assert pk is not None, "PK task should exist"
        pk_log = pk.get("timeLog") or {}
        assert pk_log.get("start") is not None, "PK timeLog.start"
        assert pk_log.get("end") is not None, "PK timeLog.end"

        # ST task — should have timeLog with start and end
        _, st = api.jobs.tasks.get_task(JOB, "ST")
        assert st is not None, "ST task should exist"
        st_log = st.get("timeLog") or {}
        assert st_log.get("start") is not None, "ST timeLog.start"
        assert st_log.get("end") is not None, "ST timeLog.end"

        # CP task — all three carrier dates should be preserved
        _, cp = api.jobs.tasks.get_task(JOB, "CP")
        assert cp is not None, "CP task should exist"
        assert cp.get("scheduledDate") is not None, "CP scheduledDate"
        assert cp.get("pickupCompletedDate") is not None, "CP pickupCompletedDate"
        assert cp.get("deliveryCompletedDate") is not None, "CP deliveryCompletedDate"


class TestTimelineRollbackBehavior:
    """Focused live repros for backward timeline transitions."""

    def test_patch_packaging_completed_back_to_started_requires_deleting_pk(self, api):
        """PATCH PK from status 5 to 4 is rejected; deleting PK rolls status back.

        Repro sequence:
        1. delete all timeline tasks
        2. create PU received (status 3)
        3. create PK started/completed with a timeLog (status 5)
        4. PATCH the PK task to status 4 with ``completedDate: null``
        5. delete PK to roll the job back to status 3
        """
        api.jobs.tasks.delete_all(JOB)

        try:
            received = api.jobs.tasks.received(
                JOB,
                start=TEST_PU_START_DATE,
                end=TEST_PU_END_DATE,
            )
            assert received.success is True
            assert _current_status_code(api, JOB) == 3

            pack_started = api.jobs.tasks.pack_start(JOB, start=TEST_PK_START_DATE)
            assert pack_started.success is True
            pack_finished = api.jobs.tasks.pack_finish(JOB, end=TEST_PK_END_DATE)
            assert pack_finished.success is True
            assert _current_status_code(api, JOB) == 5

            _, pk = api.jobs.tasks.get_task(JOB, "PK")
            assert pk is not None
            pk_id = pk.get("id")
            assert pk_id is not None

            with pytest.raises(RequestError) as exc_info:
                api.jobs.timeline._client.request(
                    "PATCH",
                    f"/job/{JOB}/timeline/{pk_id}",
                    json={"status": 4, "completedDate": None},
                )

            assert exc_info.value.status_code == 400
            assert "Task of a such type (PK) can not be updated" in exc_info.value.message
            assert _current_status_code(api, JOB) == 5

            deleted = api.jobs.tasks.delete(JOB, "PK")
            assert deleted is not None
            assert _current_status_code(api, JOB) == 3
            _, pk_after_delete = api.jobs.tasks.get_task(JOB, "PK")
            assert pk_after_delete is None
        finally:
            api.jobs.tasks.delete_all(JOB)

    def test_clear_pack_finish_reopens_packaging_without_deleting_pk(self, api):
        """clear_pack_finish() clears PK completion and keeps the same PK task."""
        api.jobs.tasks.delete_all(JOB)

        try:
            received = api.jobs.tasks.received(
                JOB,
                start=TEST_PU_START_DATE,
                end=TEST_PU_END_DATE,
            )
            assert received.success is True
            pack_started = api.jobs.tasks.pack_start(JOB, start=TEST_PK_START_DATE)
            assert pack_started.success is True
            pack_finished = api.jobs.tasks.pack_finish(JOB, end=TEST_PK_END_DATE)
            assert pack_finished.success is True
            assert _current_status_code(api, JOB) == 5

            _, pk_before = api.jobs.tasks.get_task(JOB, "PK")
            assert pk_before is not None
            pk_id = pk_before.get("id")
            assert pk_id is not None

            reopened = api.jobs.tasks.clear_pack_finish(JOB)

            assert reopened.success is True
            assert _current_status_code(api, JOB) == 4
            _, pk_after = api.jobs.tasks.get_task(JOB, "PK")
            assert pk_after is not None
            assert pk_after.get("id") == pk_id
            time_log = pk_after.get("timeLog") or {}
            assert time_log.get("start") is not None
            assert time_log.get("end") is None
        finally:
            api.jobs.tasks.delete_all(JOB)


def _current_status_code(api, job_id: int) -> int:
    """Return the integer status code from ``jobSubManagementStatus.name``."""
    status_info, _ = api.jobs.tasks.get_task(job_id, "PU")
    name = status_info.get("name") or ""
    return int(float(name.split(" - ", 1)[0]))
