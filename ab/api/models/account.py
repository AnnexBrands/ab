"""Account models for the ACPortal API.

Covers registration, confirmation, password reset/set,
profile, and payment source endpoints under /api/account/.
"""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


# ---- Response Models --------------------------------------------------------


class AccountResponse(ResponseModel):
    """Account operation response — POST /account/register."""

    success: Optional[bool] = Field(None, description="Whether the operation succeeded")
    message: Optional[str] = Field(None, description="Response message")
    user_id: Optional[str] = Field(None, alias="userId", description="User ID")


class TokenVerification(ResponseModel):
    """Token verification result — GET /account/verifyresettoken."""

    is_valid: Optional[bool] = Field(None, alias="isValid", description="Whether the token is valid")
    username: Optional[str] = Field(None, description="Username associated with token")


class UserProfile(ResponseModel):
    """User profile — GET /account/profile."""

    id: Optional[str] = Field(None, description="User ID")
    username: Optional[str] = Field(None, description="Username")
    email: Optional[str] = Field(None, description="Email address")
    first_name: Optional[str] = Field(None, alias="firstName", description="First name")
    last_name: Optional[str] = Field(None, alias="lastName", description="Last name")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company ID")
    roles: Optional[List[str]] = Field(None, description="User roles")


class AccountPaymentSource(ResponseModel):
    """Payment source — PUT /account/paymentsource/{sourceId}."""

    id: Optional[str] = Field(None, description="Payment source ID")
    source_type: Optional[str] = Field(None, alias="sourceType", description="Payment source type")
    last4: Optional[str] = Field(None, description="Last 4 digits")


# ---- Request Models ---------------------------------------------------------


class RegisterRequest(RequestModel):
    """Body for POST /account/register."""

    username: Optional[str] = Field(None, description="Username")
    email: Optional[str] = Field(None, description="Email address")
    password: Optional[str] = Field(None, description="Password")
    first_name: Optional[str] = Field(None, alias="firstName", description="First name")
    last_name: Optional[str] = Field(None, alias="lastName", description="Last name")


class SendConfirmationRequest(RequestModel):
    """Body for POST /account/sendConfirmation."""

    email: Optional[str] = Field(None, description="Email address to send confirmation to")


class ConfirmRequest(RequestModel):
    """Body for POST /account/confirm."""

    token: Optional[str] = Field(None, description="Confirmation token")
    username: Optional[str] = Field(None, description="Username")


class ForgotRequest(RequestModel):
    """Body for POST /account/forgot."""

    email: Optional[str] = Field(None, description="Email address for password reset")


class ResetPasswordRequest(RequestModel):
    """Body for POST /account/resetpassword."""

    username: Optional[str] = Field(None, description="Username")
    token: Optional[str] = Field(None, description="Reset token")
    new_password: Optional[str] = Field(None, alias="newPassword", description="New password")


class SetPasswordRequest(RequestModel):
    """Body for POST /account/setpassword."""

    current_password: Optional[str] = Field(None, alias="currentPassword", description="Current password")
    new_password: Optional[str] = Field(None, alias="newPassword", description="New password")


class PaymentSourceRequest(RequestModel):
    """Body for PUT /account/paymentsource/{sourceId}."""

    source_type: Optional[str] = Field(None, alias="sourceType", description="Payment source type")
    token: Optional[str] = Field(None, description="Payment token")
