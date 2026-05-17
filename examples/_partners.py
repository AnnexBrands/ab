"""Example: Partner operations (3 methods).

Covers list, get, and search.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Partners", env="staging")

TEST_PARTNER_ID = "PLACEHOLDER"

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
    lambda api: api.partners.get(TEST_PARTNER_ID),
    response_model="Partner",
    fixture_file="Partner.json",
)

runner.add(
    "search",
    lambda api, data=None: api.partners.search(data=data or {}),
    request_model="PartnerSearchRequest",
    request_fixture_file="PartnerSearchRequest.json",
    response_model="List[Partner]",
    fixture_file="Partner.json",
)

if __name__ == "__main__":
    runner.run()
