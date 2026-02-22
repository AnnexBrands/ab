from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

new_elabel = api.companies.get_fulldetails("LA6190")
curr_elabel = api.companies.get_fulldetails(
    "78a6b105-b59b-ec11-822e-a4aa13c701a3"
)  # LA5636


fields = [
    # (row_label,                                   accessor)
    ("details.parentId",                             lambda c: c.details and c.details.parent_id),
    ("details.companyTypeId",                        lambda c: c.details and c.details.company_type_id),
    ("preferences.pricingToUse",                     lambda c: c.preferences and c.preferences.pricing_to_use),
    ("preferences.carrierAccountsSourceCompanyId",   lambda c: c.preferences and c.preferences.carrier_accounts_source_company_id),
    ("preferences.copyMaterials",                    lambda c: c.preferences and c.preferences.copy_materials),
    ("capabilities",                                 lambda c: c.capabilities),
]

# ── build rows ──────────────────────────────────────────────────────
rows = []
for label, fn in fields:
    nv = str(fn(new_elabel) or "—")
    cv = str(fn(curr_elabel) or "—")
    rows.append((label, nv, cv))

# ── column widths ───────────────────────────────────────────────────
hdr_field, hdr_new, hdr_curr = "Field", "LA6190 (new)", "LA5636 (curr)"
w0 = max(len(hdr_field), *(len(r[0]) for r in rows))
w1 = max(len(hdr_new),   *(len(r[1]) for r in rows))
w2 = max(len(hdr_curr),  *(len(r[2]) for r in rows))

sep = f"+-{'-'*w0}-+-{'-'*w1}-+-{'-'*w2}-+"
fmt = lambda a, b, c: f"| {a:<{w0}} | {b:<{w1}} | {c:<{w2}} |"

# ── print ───────────────────────────────────────────────────────────
print(sep)
print(fmt(hdr_field, hdr_new, hdr_curr))
print(sep)
for label, nv, cv in rows:
    print(fmt(label, nv, cv))
print(sep)

# new_elabel.preferences.carrier_accounts_source_company_id = None
# r = api.companies.update_fulldetails("LA6190", preferences={"carrierAccountsSourceCompanyId": None}) ## HTTP500