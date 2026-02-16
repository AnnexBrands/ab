"""Example: Company Setup operations (26 endpoints)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Company Setup", env="staging")

LIVE_COMPANY_UUID = "93179b52-3da9-e311-b6f8-000c298b59ee"

# ── Calendar ─────────────────────────────────────────────────────────

runner.add(
    "get_calendar",
    lambda api: api.company_setup.get_calendar(LIVE_COMPANY_UUID, "2026-02-14"),
    response_model="CalendarDay",
    fixture_file="CalendarDay.json",
)

runner.add(
    "get_calendar_baseinfo",
    lambda api: api.company_setup.get_calendar_baseinfo(LIVE_COMPANY_UUID, "2026-02-14"),
    response_model="CalendarBaseInfo",
    fixture_file="CalendarBaseInfo.json",
)

runner.add(
    "get_calendar_startofday",
    lambda api: api.company_setup.get_calendar_startofday(LIVE_COMPANY_UUID, "2026-02-14"),
    response_model="CalendarTimeInfo",
    fixture_file="CalendarTimeInfo.json",
)

runner.add(
    "get_calendar_endofday",
    lambda api: api.company_setup.get_calendar_endofday(LIVE_COMPANY_UUID, "2026-02-14"),
    response_model="CalendarTimeInfo",
)

# ── Document Templates ───────────────────────────────────────────────

runner.add(
    "get_document_templates",
    lambda api: api.company_setup.get_document_templates(LIVE_COMPANY_UUID),
    response_model="List[DocumentTemplate]",
    fixture_file="DocumentTemplate.json",
)

# ── Grid/Setup Settings ─────────────────────────────────────────────

runner.add(
    "get_grid_settings",
    lambda api: api.company_setup.get_grid_settings(LIVE_COMPANY_UUID),
    response_model="GridSettings",
    fixture_file="GridSettings.json",
)

runner.add(
    "get_setup_data",
    lambda api: api.company_setup.get_setup_data(LIVE_COMPANY_UUID),
    response_model="CompanySetupData",
    fixture_file="CompanySetupData.json",
)

# ── Container Thickness ─────────────────────────────────────────────

runner.add(
    "get_container_thickness",
    lambda api: api.company_setup.get_container_thickness(LIVE_COMPANY_UUID),
    response_model="List[ContainerThickness]",
    fixture_file="ContainerThickness.json",
)

# ── Planner ──────────────────────────────────────────────────────────

runner.add(
    "get_planner",
    lambda api: api.company_setup.get_planner(LIVE_COMPANY_UUID),
    response_model="List[PlannerEntry]",
    fixture_file="PlannerEntry.json",
)

# ── Material ─────────────────────────────────────────────────────────

runner.add(
    "get_materials",
    lambda api: api.company_setup.get_materials(LIVE_COMPANY_UUID),
    response_model="List[Material]",
    fixture_file="Material.json",
)

# ── Truck ────────────────────────────────────────────────────────────

runner.add(
    "get_trucks",
    lambda api: api.company_setup.get_trucks(LIVE_COMPANY_UUID),
    response_model="List[Truck]",
    fixture_file="Truck.json",
)

if __name__ == "__main__":
    runner.run()
