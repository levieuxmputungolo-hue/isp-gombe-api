from datetime import datetime
from sqlalchemy.orm import Session
from app.models_payment import ResultAccess, Payment, PaymentConfig


def get_access_duration_days(db: Session) -> int:
    config = db.query(PaymentConfig).filter(PaymentConfig.key == "access_duration_days").first()
    if config:
        try:
            return int(config.value)
        except (ValueError, TypeError):
            pass
    return 30


def get_consultation_fee(db: Session) -> float:
    config = db.query(PaymentConfig).filter(PaymentConfig.key == "consultation_fee").first()
    if config:
        try:
            return float(config.value)
        except (ValueError, TypeError):
            pass
    return 5000.0


def get_currency(db: Session) -> str:
    config = db.query(PaymentConfig).filter(PaymentConfig.key == "currency").first()
    if config:
        return config.value
    return "CDF"


def check_student_access(db: Session, student_name: str, promotion: str, level: str, option: str = "", section: str = "") -> dict:
    now = datetime.utcnow()

    access = (
        db.query(ResultAccess)
        .filter(
            ResultAccess.student_name.ilike(f"%{student_name}%"),
            ResultAccess.student_promotion == promotion,
            ResultAccess.student_level == level,
            ResultAccess.is_active == True,
            ResultAccess.expires_at > now,
        )
        .order_by(ResultAccess.expires_at.desc())
        .first()
    )

    if access:
        days_remaining = (access.expires_at - now).days
        return {
            "has_access": True,
            "expires_at": access.expires_at.isoformat(),
            "days_remaining": days_remaining,
            "access_id": access.id,
        }

    return {"has_access": False, "expires_at": None, "days_remaining": 0}


def grant_access(db: Session, payment: Payment) -> ResultAccess:
    now = datetime.utcnow()
    duration_days = get_access_duration_days(db)

    access = ResultAccess(
        student_name=payment.student_name,
        student_promotion=payment.student_promotion,
        student_level=payment.student_level,
        student_option=payment.student_option,
        student_section=payment.student_section,
        payment_id=payment.id,
        access_type="RESULTS_AND_TRANSCRIPT",
        started_at=now,
        expires_at=now.replace(hour=23, minute=59, second=59) + __import__("datetime").timedelta(days=duration_days),
        is_active=True,
    )
    db.add(access)
    db.commit()
    db.refresh(access)
    return access


def init_default_config(db: Session):
    defaults = [
        ("consultation_fee", "5000", "Frais de consultation des résultats (CDF)"),
        ("currency", "CDF", "Devise du paiement"),
        ("access_duration_days", "30", "Durée d'accès après paiement (jours)"),
        ("mpesa_enabled", "true", "Activer M-Pesa"),
        ("airtel_enabled", "true", "Activer Airtel Money"),
        ("orange_enabled", "true", "Activer Orange Money"),
    ]

    for key, value, description in defaults:
        existing = db.query(PaymentConfig).filter(PaymentConfig.key == key).first()
        if not existing:
            db.add(PaymentConfig(key=key, value=value, description=description))
    db.commit()
