from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreatePaymentRequest(BaseModel):
    student_name: str
    promotion: str
    level: str
    option: str = ""
    section: str = ""
    provider: str  # MPESA, AIRTEL_MONEY, ORANGE_MONEY
    phone_number: str
    purpose: str = "RESULTS_ACCESS"


class PaymentOut(BaseModel):
    id: int
    reference: str
    student_name: str
    provider: str
    phone_number: str
    amount: float
    currency: str
    purpose: str
    status: str
    error_message: str = ""
    created_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaymentStatusResponse(BaseModel):
    reference: str
    status: str
    amount: float
    currency: str
    provider: str
    message: str


class AccessCheckResponse(BaseModel):
    has_access: bool
    expires_at: Optional[datetime] = None
    days_remaining: int = 0


class PaymentConfigOut(BaseModel):
    key: str
    value: str
    description: str

    class Config:
        from_attributes = True


class UpdateConfigRequest(BaseModel):
    key: str
    value: str


class PaymentHistoryItem(BaseModel):
    reference: str
    provider: str
    amount: float
    currency: str
    purpose: str
    status: str
    created_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None


class AdminDashboardStats(BaseModel):
    total_today: float
    total_week: float
    total_month: float
    count_total: int
    count_success: int
    count_pending: int
    count_failed: int


class AdminPaymentRow(BaseModel):
    id: int
    reference: str
    student_name: str
    provider: str
    amount: float
    currency: str
    status: str
    created_at: Optional[datetime] = None


class WebhookPayload(BaseModel):
    reference: str
    transaction_id: str
    status: str
    amount: float
    phone_number: str
