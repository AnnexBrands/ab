"""Example: Contacts operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_contacts.py) to the plain-script form.

See also: https://ab-sdk.readthedocs.io/en/latest/api/contacts.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_CONTACT_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /contacts/{id}
    print("\n# api.contacts.get(...)")
    result = api.contacts.get(str(TEST_CONTACT_ID))
    print(format_result(result))
    save("ContactSimple.json", result)

    # GET /contacts/user
    print("\n# api.contacts.get_current_user()")
    result = api.contacts.get_current_user()
    print(format_result(result))
    save("ContactSimple.json", result)

    # GET /contacts/{contactId}/editdetails
    print("\n# api.contacts.get_details(...)")
    result = api.contacts.get_details(str(TEST_CONTACT_ID))
    print(format_result(result))
    save("ContactDetailedInfo.json", result)

    # GET /contacts/{contactId}/primarydetails
    print("\n# api.contacts.get_primary_details(...)")
    result = api.contacts.get_primary_details(str(TEST_CONTACT_ID))
    print(format_result(result))
    save("ContactPrimaryDetails.json", result)

    # POST /contacts/v2/search — read-only search, safe to run unguarded.
    print("\n# api.contacts.search(data=ContactSearchRequest(...))")
    result = api.contacts.search(data=load_request("ContactSearchRequest.json"))
    print(format_result(result))
    save("SearchContactEntityResult.json", result)

    # POST /contacts/editdetails — creates a contact (mutating).
    print("\n# api.contacts.create(data=ContactEditRequest(...))")
    if mutations_enabled():
        result = api.contacts.create(data=load_request("ContactEditRequest.json"))
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # PUT /contacts/{contactId}/editdetails — updates a contact (mutating).
    print("\n# api.contacts.update_details(..., data=ContactEditRequest(...))")
    if mutations_enabled():
        result = api.contacts.update_details(
            str(TEST_CONTACT_ID), data=load_request("ContactEditRequest.json")
        )
        print(format_result(result))
    else:
        print("  skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
