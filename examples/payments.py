"""Example: Payment operations (10 methods)."""

from examples._runner import ExampleRunner
from tests.constants import TEST_JOB_DISPLAY_ID

runner = ExampleRunner("Payments", env="staging")

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get",
    lambda api: api.payments.get(TEST_JOB_DISPLAY_ID),
    response_model="PaymentInfo",
)

runner.add(
    "get_create",
    lambda api: api.payments.get_create(TEST_JOB_DISPLAY_ID),
    response_model="PaymentInfo",
)

runner.add(
    "get_sources",
    lambda api: api.payments.get_sources(TEST_JOB_DISPLAY_ID),
    response_model="List[PaymentSource]",
)

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "pay_by_source",
    lambda api, data=None: api.payments.pay_by_source(TEST_JOB_DISPLAY_ID, data or {}),
    request_model="PayBySourceRequest",
    request_fixture_file="PayBySourceRequest.json",
    response_model="ServiceBaseResponse",
)

runner.add(
    "create_ach_session",
    lambda api, data=None: api.payments.create_ach_session(TEST_JOB_DISPLAY_ID, data or {}),
    request_model="ACHSessionRequest",
    request_fixture_file="ACHSessionRequest.json",
    response_model="ACHSessionResponse",
)

runner.add(
    "ach_credit_transfer",
    lambda api, data=None: api.payments.ach_credit_transfer(TEST_JOB_DISPLAY_ID, data or {}),
    request_model="ACHCreditTransferRequest",
    request_fixture_file="ACHCreditTransferRequest.json",
    response_model="ServiceBaseResponse",
)

runner.add(
    "attach_customer_bank",
    lambda api, data=None: api.payments.attach_customer_bank(TEST_JOB_DISPLAY_ID, data or {}),
    request_model="AttachBankRequest",
    request_fixture_file="AttachBankRequest.json",
    response_model="ServiceBaseResponse",
)

runner.add(
    "verify_ach_source",
    lambda api, data=None: api.payments.verify_ach_source(TEST_JOB_DISPLAY_ID, data or {}),
    request_model="VerifyACHRequest",
    request_fixture_file="VerifyACHRequest.json",
    response_model="ServiceBaseResponse",
)

runner.add(
    "cancel_ach_verification",
    lambda api: api.payments.cancel_ach_verification(TEST_JOB_DISPLAY_ID),
    response_model="ServiceBaseResponse",
)

runner.add(
    "set_bank_source",
    lambda api, data=None: api.payments.set_bank_source(TEST_JOB_DISPLAY_ID, data or {}),
    request_model="BankSourceRequest",
    request_fixture_file="BankSourceRequest.json",
    response_model="ServiceBaseResponse",
)

if __name__ == "__main__":
    runner.run()
