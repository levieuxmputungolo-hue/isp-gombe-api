import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db import Base


class PaymentConfig(Base):
    __tablename__ = "payment_config"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    description = Column(Text, default="")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(50), unique=True, nullable=False, index=True)
    student_name = Column(String(200), nullable=False, index=True)
    student_promotion = Column(String(50), nullable=False)
    student_level = Column(String(20), nullable=False)
    student_option = Column(String(200), default="")
    student_section = Column(String(200), default="")

    provider = Column(String(20), nullable=False)  # MPESA, AIRTEL_MONEY, ORANGE_MONEY
    phone_number = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="CDF")
    purpose = Column(String(50), nullable=False)  # RESULTS_ACCESS, TRANSCRIPT_ACCESS

    status = Column(String(20), default="PENDING", index=True)
    # PENDING, SUCCESS, FAILED, EXPIRED, CANCELLED, REFUNDED

    provider_transaction_id = Column(String(200), default="")
    provider_reference = Column(String(200), default="")
    error_message = Column(Text, default="")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    access = relationship("ResultAccess", back_populates="payment", uselist=False)


class ResultAccess(Base):
    __tablename__ = "result_access"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(200), nullable=False, index=True)
    student_promotion = Column(String(50), nullable=False)
    student_level = Column(String(20), nullable=False)
    student_option = Column(String(200), default="")
    student_section = Column(String(200), default="")

    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    access_type = Column(String(50), default="RESULTS_AND_TRANSCRIPT")
    started_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    payment = relationship("Payment", back_populates="access")


class PaymentAudit(Base):
    __tablename__ = "payment_audit"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    reference = Column(String(50), nullable=False, index=True)
    event = Column(String(50), nullable=False)
    # payment_created, payment_initiated, payment_pending, payment_success,
    # payment_failed, payment_expired, payment_refunded, access_granted
    details = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


def generate_payment_reference():
    now = datetime.utcnow()
    unique_id = str(uuid.uuid4().int)[:6]
    return f"PAY-{now.year}-{unique_id.zfill(6)}"
