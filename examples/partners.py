"""Example: Partner operations (3 methods).

Covers list, get, and search.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Partners", env="staging")

LIVE_PARTNER_ID = "PLACEHOLDER"

# ═══════════════════════════════════════════════════════════════════════
# Partners
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "list",
    lambda api: api.partners.list(),
    response_model="List[Partner]",
    fixture_file="Partner.json",
)

runner.add(
    "get",
    lambda api: api.partners.get(LIVE_PARTNER_ID),
    response_model="Partner",
)

runner.add(
    "search",
    lambda api, data=None: api.partners.search(**(data or {})),
    request_model="PartnerSearchRequest",
    request_fixture_file="PartnerSearchRequest.json",
    response_model="List[Partner]",
)

if __name__ == "__main__":
    runner.run()
