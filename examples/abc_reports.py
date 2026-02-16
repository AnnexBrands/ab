"""Example: ABC Reports operations (2 endpoints)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("ABC Reports", env="staging")

runner.add(
    "get_web_revenue",
    lambda api: api.abc_reports.get_web_revenue(
        accessKey="test-key",
        startDate="2026-01-01",
        endDate="2026-02-14",
    ),
)

runner.add(
    "flush_log_buffer",
    lambda api: api.abc_reports.flush_log_buffer(),
)

if __name__ == "__main__":
    runner.run()
