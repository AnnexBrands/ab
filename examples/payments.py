"""Example: Payment operations (10 methods)."""

from examples._runner import ExampleRunner
from tests.constants import LIVE_JOB_DISPLAY_ID

runner = ExampleRunner("Payments", env="staging")

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get",
    lambda api: api.payments.get(
        # TODO: capture fixture — needs job ID with payment data
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="PaymentInfo",
)

runner.add(
    "get_create",
    lambda api: api.payments.get_create(
        # TODO: capture fixture — needs job ID with payment data
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="PaymentInfo",
)

runner.add(
    "get_sources",
    lambda api: api.payments.get_sources(
        # TODO: capture fixture — needs job ID with payment sources
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="List[PaymentSource]",
)

runner.add(
    "pay_by_source",
    lambda api: api.payments.pay_by_source(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid PayBySourceRequest body
        {},
    ),
    request_model="PayBySourceRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "create_ach_session",
    lambda api: api.payments.create_ach_session(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid ACHSessionRequest body
        {},
    ),
    request_model="ACHSessionRequest",
    response_model="ACHSessionResponse",
)

runner.add(
    "ach_credit_transfer",
    lambda api: api.payments.ach_credit_transfer(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid ACHCreditTransferRequest body
        {},
    ),
    request_model="ACHCreditTransferRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "attach_customer_bank",
    lambda api: api.payments.attach_customer_bank(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid AttachBankRequest body
        {},
    ),
    request_model="AttachBankRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "verify_ach_source",
    lambda api: api.payments.verify_ach_source(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid VerifyACHRequest body
        {},
    ),
    request_model="VerifyACHRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "cancel_ach_verification",
    lambda api: api.payments.cancel_ach_verification(
        # TODO: capture fixture — needs job ID with active ACH verification
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="ServiceBaseResponse",
)

runner.add(
    "set_bank_source",
    lambda api: api.payments.set_bank_source(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid BankSourceRequest body
        {},
    ),
    request_model="BankSourceRequest",
    response_model="ServiceBaseResponse",
)

if __name__ == "__main__":
    runner.run()
