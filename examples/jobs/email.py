"""Example: api.jobs.email — transactional / document / template sends.

Live SDK example — real call, real printed pydantic response. Authored for
feature 037 (endpoints previously had no example).

All three calls here are state-changing (they dispatch real email from
staging), so each is wrapped in ``mutations_enabled()``; set
``AB_RUN_MUTATIONS=1`` to run them. None of these routes return a response
model (swagger ``->`` no schema), so there is nothing to save as a fixture.

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled
from examples.constants import TEST_JOB_DISPLAY_ID

# Path param for send_template: the GUID of the email template to dispatch.
# No master-constant lookup is exposed for this in the SDK, so an operator must
# supply a real emailTemplateGuid (from the platform's template admin) for a
# live run. The legacy examples/_email_sms.py used the same literal placeholder.
TEMPLATE_GUID = "TEMPLATE_GUID"


def main() -> None:
    api = ABConnectAPI(env="staging")

    # All calls below dispatch real email — guarded so a default run and the
    # verify harness exercise nothing. Set AB_RUN_MUTATIONS=1 to run them.
    if not mutations_enabled():
        print(
            "# api.jobs.email.{create_transactional,send_document,send_template} "
            "skipped — set AB_RUN_MUTATIONS=1 to run (sends email from staging)",
        )
        return

    # POST /job/{jobDisplayId}/email/createtransactionalemail — no body, no response model.
    print(f"\n# api.jobs.email.create_transactional({TEST_JOB_DISPLAY_ID})")
    result = api.jobs.email.create_transactional(TEST_JOB_DISPLAY_ID)
    print(format_result(result))

    # POST /job/{jobDisplayId}/email/senddocument — SendDocumentEmailModel body, no response model.
    print(f"\n# api.jobs.email.send_document({TEST_JOB_DISPLAY_ID}, data=...)")
    result = api.jobs.email.send_document(
        TEST_JOB_DISPLAY_ID,
        data=load_request("SendDocumentEmailModel.json"),
    )
    print(format_result(result))

    # POST /job/{jobDisplayId}/email/{emailTemplateGuid}/send — template GUID path param, no response model.
    print(f"\n# api.jobs.email.send_template({TEST_JOB_DISPLAY_ID}, {TEMPLATE_GUID!r})")
    result = api.jobs.email.send_template(TEST_JOB_DISPLAY_ID, TEMPLATE_GUID)
    print(format_result(result))


if __name__ == "__main__":
    main()
