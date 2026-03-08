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

        # Verify PU task now has completed date
        _, task = api.jobs.tasks.get_task(JOB, "PU")
        assert task is not None
        assert task.get("completedDate") is not None, "PU completedDate should be set"

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
        """Carrier pickup — upserts existing CP task with pickup date."""
        resp = api.jobs.tasks.carrier_pickup(JOB, start=TEST_TR_PICKUP_COMPLETED_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        _, task = api.jobs.tasks.get_task(JOB, "CP")
        assert task is not None
        assert task.get("pickupCompletedDate") is not None, "CP pickupCompletedDate should be set"

    def test_step_10_carrier_delivery(self, api):
        """Carrier delivery — upserts existing CP task with delivery date."""
        resp = api.jobs.tasks.carrier_delivery(JOB, end=TEST_TR_DELIVERY_COMPLETED_DATE)
        assert isinstance(resp, TimelineSaveResponse)
        assert resp.success is True

        _, task = api.jobs.tasks.get_task(JOB, "CP")
        assert task is not None
        assert task.get("deliveryCompletedDate") is not None, "CP deliveryCompletedDate should be set"

    def test_step_11_verify_final_state(self, api):
        """Verify all 4 task types have expected dates after full sequence."""
        # PU task — received() overwrites the task so plannedStartDate may
        # not survive, but completedDate must be present
        _, pu = api.jobs.tasks.get_task(JOB, "PU")
        assert pu is not None, "PU task should exist"
        assert pu.get("completedDate") is not None, "PU completedDate"

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

        # CP task — each carrier helper upserts with its own field;
        # the server preserves only the last-written fields.
        # deliveryCompletedDate should be set (last carrier helper called).
        _, cp = api.jobs.tasks.get_task(JOB, "CP")
        assert cp is not None, "CP task should exist"
        assert cp.get("deliveryCompletedDate") is not None, "CP deliveryCompletedDate"
