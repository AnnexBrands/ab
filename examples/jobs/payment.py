"""Example: api.jobs.payment — job-scoped payment operations (swagger tag JobPayment).

Live SDK example — real call, real printed pydantic response. Authored for
feature 037 (endpoint previously had no example). These routes were moved here
from the legacy ``api.payments.*`` surface (same method names); the working call
shapes and request fixtures are reused from ``examples/_payments.py``.

Read-only GETs run by default. The state-changing POSTs (ACH session, attach
bank, credit transfer, pay-by-source, set/verify bank source, cancel ACH
verification) mutate staging and are guarded — set ``AB_RUN_MUTATIONS=1`` to run
them.

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # --- Read-only: payment info / create form / saved sources ----------
    print(f"\n# api.jobs.payment.get({TEST_JOB_DISPLAY_ID})")
    info = api.jobs.payment.get(TEST_JOB_DISPLAY_ID)
    print(format_result(info))
    save("PaymentInfo.json", info)

    print(f"\n# api.jobs.payment.get_create({TEST_JOB_DISPLAY_ID})")
    create_info = api.jobs.payment.get_create(TEST_JOB_DISPLAY_ID)
    print(format_result(create_info))
    save("PaymentInfo.json", create_info)

    print(f"\n# api.jobs.payment.get_sources({TEST_JOB_DISPLAY_ID})")
    sources = api.jobs.payment.get_sources(TEST_JOB_DISPLAY_ID)
    print(format_result(sources))
    save("PaymentSource.json", sources)

    # --- State-changing — guarded ---------------------------------------
    if not mutations_enabled():
        print(
            "\n# api.jobs.payment mutations skipped "
            "(create_ach_session, cancel_ach_verification, attach_customer_bank, "
            "ach_credit_transfer, pay_by_source, set_bank_source, verify_ach_source) "
            "— set AB_RUN_MUTATIONS=1 to run (mutates staging)"
        )
        return

    print(f"\n# api.jobs.payment.create_ach_session({TEST_JOB_DISPLAY_ID}, data=ACHSessionRequest(...))")
    ach_session = api.jobs.payment.create_ach_session(
        TEST_JOB_DISPLAY_ID, data=load_request("ACHSessionRequest.json")
    )
    print(format_result(ach_session))
    save("ACHSessionResponse.json", ach_session)

    print(f"\n# api.jobs.payment.cancel_ach_verification({TEST_JOB_DISPLAY_ID})")
    cancelled = api.jobs.payment.cancel_ach_verification(TEST_JOB_DISPLAY_ID)
    print(format_result(cancelled))
    save("ServiceBaseResponse.json", cancelled)

    print(f"\n# api.jobs.payment.attach_customer_bank({TEST_JOB_DISPLAY_ID}, data=AttachBankRequest(...))")
    attached = api.jobs.payment.attach_customer_bank(
        TEST_JOB_DISPLAY_ID, data=load_request("AttachBankRequest.json")
    )
    print(format_result(attached))
    save("ServiceBaseResponse.json", attached)

    print(f"\n# api.jobs.payment.ach_credit_transfer({TEST_JOB_DISPLAY_ID}, data=ACHCreditTransferRequest(...))")
    transferred = api.jobs.payment.ach_credit_transfer(
        TEST_JOB_DISPLAY_ID, data=load_request("ACHCreditTransferRequest.json")
    )
    print(format_result(transferred))

    print(f"\n# api.jobs.payment.pay_by_source({TEST_JOB_DISPLAY_ID}, data=PayBySourceRequest(...))")
    paid = api.jobs.payment.pay_by_source(
        TEST_JOB_DISPLAY_ID, data=load_request("PayBySourceRequest.json")
    )
    print(format_result(paid))

    print(f"\n# api.jobs.payment.set_bank_source({TEST_JOB_DISPLAY_ID}, data=BankSourceRequest(...))")
    bank_set = api.jobs.payment.set_bank_source(
        TEST_JOB_DISPLAY_ID, data=load_request("BankSourceRequest.json")
    )
    print(format_result(bank_set))

    print(f"\n# api.jobs.payment.verify_ach_source({TEST_JOB_DISPLAY_ID}, data=VerifyACHRequest(...))")
    verified = api.jobs.payment.verify_ach_source(
        TEST_JOB_DISPLAY_ID, data=load_request("VerifyACHRequest.json")
    )
    print(format_result(verified))


if __name__ == "__main__":
    main()
