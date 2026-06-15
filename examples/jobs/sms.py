"""Example: api.jobs.sms — list / get template / send / mark read.

Live SDK example — real call, real printed pydantic response. Authored for
feature 037 (endpoint previously had no example).

The SMS routes return no pydantic model (``resp=-`` in swagger), so the GET
calls print only and nothing is saved. The two state-changing calls (``send``
and ``mark_read``) are guarded behind ``AB_RUN_MUTATIONS=1`` and post real
request bodies loaded from the committed request fixtures.

Method renames vs. the legacy ``examples/_email_sms.py``: ``list_sms`` -> ``list``,
``get_sms_template`` -> ``get_template``, ``send_sms`` -> ``send``,
``mark_sms_read`` -> ``mark_read``.

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled
from examples.constants import TEST_JOB_DISPLAY_ID, TEST_SMS_TEMPLATE_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /job/{jobDisplayId}/sms — list SMS messages (no model → print only).
    print(f"\n# api.jobs.sms.list({TEST_JOB_DISPLAY_ID})")
    result = api.jobs.sms.list(TEST_JOB_DISPLAY_ID)
    print(format_result(result))

    # GET /job/{jobDisplayId}/sms/templatebased/{templateId} — template id is a
    # path string (no model → print only).
    print(f"\n# api.jobs.sms.get_template({TEST_JOB_DISPLAY_ID}, {str(TEST_SMS_TEMPLATE_ID)!r})")
    result = api.jobs.sms.get_template(TEST_JOB_DISPLAY_ID, str(TEST_SMS_TEMPLATE_ID))
    print(format_result(result))

    # State-changing — guarded. No response model, so nothing is saved.
    if mutations_enabled():
        print(f"\n# api.jobs.sms.send({TEST_JOB_DISPLAY_ID}, data=SendSMSModel(...))")
        res = api.jobs.sms.send(TEST_JOB_DISPLAY_ID, data=load_request("SendSMSModel.json"))
        print(format_result(res))

        print(f"\n# api.jobs.sms.mark_read({TEST_JOB_DISPLAY_ID}, data=MarkSmsAsReadModel(...))")
        res = api.jobs.sms.mark_read(
            TEST_JOB_DISPLAY_ID, data=load_request("MarkSmsAsReadModel.json")
        )
        print(format_result(res))
    else:
        print(
            "\n# api.jobs.sms.send / mark_read skipped — "
            "set AB_RUN_MUTATIONS=1 to run (mutates staging)"
        )


if __name__ == "__main__":
    main()
