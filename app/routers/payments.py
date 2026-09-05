from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.models_payment import Payment, ResultAccess, PaymentAudit, PaymentConfig, generate_payment_reference
from app.schemas_payment import (
    CreatePaymentRequest, PaymentOut, PaymentStatusResponse,
    AccessCheckResponse, PaymentConfigOut, UpdateConfigRequest,
    PaymentHistoryItem, AdminDashboardStats, AdminPaymentRow, WebhookPayload,
)
from app.payment_providers import get_provider, get_all_providers_status
from app.access_control import (
    check_student_access, grant_access, get_consultation_fee,
    get_currency, get_access_duration_days, init_default_config,
)
from app.models_payment import PaymentAudit

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.on_event("startup")
def startup():
    from app.db import SessionLocal
    db = SessionLocal()
    try:
        init_default_config(db)
    finally:
        db.close()


@router.get("/config")
def get_payment_config(db: Session = Depends(get_db)):
    fee = get_consultation_fee(db)
    currency = get_currency(db)
    duration = get_access_duration_days(db)
    providers = get_all_providers_status()
    return {
        "fee": fee,
        "currency": currency,
        "access_duration_days": duration,
        "providers": providers,
    }


@router.post("/create", response_model=PaymentOut)
def create_payment(req: CreatePaymentRequest, db: Session = Depends(get_db)):
    fee = get_consultation_fee(db)
    currency = get_currency(db)
    reference = generate_payment_reference()

    existing = db.query(Payment).filter(Payment.reference == reference).first()
    while existing:
        reference = generate_payment_reference()
        existing = db.query(Payment).filter(Payment.reference == reference).first()

    payment = Payment(
        reference=reference,
        student_name=req.student_name,
        student_promotion=req.promotion,
        student_level=req.level,
        student_option=req.option,
        student_section=req.section,
        provider=req.provider,
        phone_number=req.phone_number,
        amount=fee,
        currency=currency,
        purpose=req.purpose,
        status="PENDING",
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(minutes=30),
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    audit = PaymentAudit(
        payment_id=payment.id,
        reference=reference,
        event="payment_created",
        details=f"Paiement créé: {fee} {currency} via {req.provider}",
    )
    db.add(audit)
    db.commit()

    provider = get_provider(req.provider)
    result = provider.initiate_payment(reference, req.phone_number, fee, currency)

    audit2 = PaymentAudit(
        payment_id=payment.id,
        reference=reference,
        event="payment_initiated",
        details=result.message,
    )
    db.add(audit2)

    if result.success:
        payment.status = "PENDING"
        payment.provider_transaction_id = result.transaction_id
        audit2.event = "payment_pending"
    else:
        payment.status = "FAILED"
        payment.error_message = result.message
        audit2.event = "payment_failed"

    db.commit()
    db.refresh(payment)

    return payment


@router.get("/{reference}", response_model=PaymentOut)
def get_payment(reference: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.reference == reference).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Paiement non trouvé")
    return payment


@router.post("/{reference}/verify", response_model=PaymentStatusResponse)
def verify_payment(reference: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.reference == reference).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Paiement non trouvé")

    if payment.status == "SUCCESS":
        return PaymentStatusResponse(
            reference=reference,
            status="SUCCESS",
            amount=payment.amount,
            currency=payment.currency,
            provider=payment.provider,
            message="Paiement déjà confirmé",
        )

    if payment.status in ("EXPIRED", "CANCELLED", "REFUNDED"):
        return PaymentStatusResponse(
            reference=reference,
            status=payment.status,
            amount=payment.amount,
            currency=payment.currency,
            provider=payment.provider,
            message=f"Paiement {payment.status.lower()}",
        )

    if payment.expires_at and payment.expires_at < datetime.utcnow():
        payment.status = "EXPIRED"
        db.commit()
        audit = PaymentAudit(payment_id=payment.id, reference=reference, event="payment_expired", details="Paiement expiré")
        db.add(audit)
        db.commit()
        return PaymentStatusResponse(
            reference=reference, status="EXPIRED", amount=payment.amount,
            currency=payment.currency, provider=payment.provider, message="Paiement expiré",
        )

    provider = get_provider(payment.provider)
    result = provider.check_status(reference, payment.provider_transaction_id)

    if result.success and "réussi" in result.message.lower() or "confirmé" in result.message.lower() or "success" in result.message.lower():
        already_granted = db.query(ResultAccess).filter(ResultAccess.payment_id == payment.id).first()
        if not already_granted:
            payment.status = "SUCCESS"
            payment.paid_at = datetime.utcnow()
            db.commit()

            access = grant_access(db, payment)

            audit = PaymentAudit(payment_id=payment.id, reference=reference, event="payment_success", details="Paiement confirmé")
            db.add(audit)
            audit2 = PaymentAudit(payment_id=payment.id, reference=reference, event="access_granted", details=f"Accès accordé jusqu'au {access.expires_at}")
            db.add(audit2)
            db.commit()

        return PaymentStatusResponse(
            reference=reference, status="SUCCESS", amount=payment.amount,
            currency=payment.currency, provider=payment.provider, message="Paiement confirmé",
        )
    elif result.success and "test" in result.message.lower():
        payment.status = "SUCCESS"
        payment.paid_at = datetime.utcnow()
        payment.provider_transaction_id = result.transaction_id
        db.commit()

        already_granted = db.query(ResultAccess).filter(ResultAccess.payment_id == payment.id).first()
        if not already_granted:
            access = grant_access(db, payment)
            audit = PaymentAudit(payment_id=payment.id, reference=reference, event="payment_success", details="Mode TEST: paiement confirmé")
            db.add(audit)
            audit2 = PaymentAudit(payment_id=payment.id, reference=reference, event="access_granted", details=f"Accès accordé jusqu'au {access.expires_at}")
            db.add(audit2)
            db.commit()

        return PaymentStatusResponse(
            reference=reference, status="SUCCESS", amount=payment.amount,
            currency=payment.currency, provider=payment.provider, message="Paiement confirmé (mode TEST)",
        )

    return PaymentStatusResponse(
        reference=reference, status="PENDING", amount=payment.amount,
        currency=payment.currency, provider=payment.provider, message=result.message,
    )


@router.post("/webhook/mpesa")
async def webhook_mpesa(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    stk_callback = body.get("Body", {}).get("stkCallback", {})
    result_code = stk_callback.get("ResultCode", -1)
    merchant_request_id = stk_callback.get("MerchantRequestID", "")
    checkout_request_id = stk_callback.get("CheckoutRequestID", "")

    callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
    amount = 0
    phone = ""
    for item in callback_metadata:
        if item.get("Name") == "Amount":
            amount = item.get("Value", 0)
        if item.get("Name") == "PhoneNumber":
            phone = item.get("Value", "")

    payment = db.query(Payment).filter(Payment.reference == merchant_request_id).first()
    if not payment:
        payment = db.query(Payment).filter(Payment.provider_transaction_id == checkout_request_id).first()

    if not payment:
        return {"status": "error", "message": "Payment not found"}

    already_processed = db.query(PaymentAudit).filter(
        PaymentAudit.payment_id == payment.id,
        PaymentAudit.event == "payment_success",
    ).first()
    if already_processed:
        return {"status": "ok", "message": "Already processed"}

    if result_code == 0:
        payment.status = "SUCCESS"
        payment.paid_at = datetime.utcnow()
        payment.provider_transaction_id = checkout_request_id
        db.commit()

        grant_access(db, payment)

        audit = PaymentAudit(payment_id=payment.id, reference=payment.reference, event="payment_success", details="Webhook M-Pesa confirmé")
        db.add(audit)
        db.commit()
    else:
        payment.status = "FAILED"
        payment.error_message = f"M-Pesa ResultCode: {result_code}"
        db.commit()

        audit = PaymentAudit(payment_id=payment.id, reference=payment.reference, event="payment_failed", details=f"Webhook M-Pesa: code {result_code}")
        db.add(audit)
        db.commit()

    return {"status": "ok"}


@router.post("/webhook/airtel")
async def webhook_airtel(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    reference = body.get("reference", "")
    status = body.get("status", "")
    transaction_id = body.get("transaction_id", "")

    payment = db.query(Payment).filter(Payment.reference == reference).first()
    if not payment:
        return {"status": "error", "message": "Payment not found"}

    already_processed = db.query(PaymentAudit).filter(
        PaymentAudit.payment_id == payment.id,
        PaymentAudit.event == "payment_success",
    ).first()
    if already_processed:
        return {"status": "ok", "message": "Already processed"}

    if status in ("SUCCESSFUL", "completed", "SUCCESS"):
        payment.status = "SUCCESS"
        payment.paid_at = datetime.utcnow()
        payment.provider_transaction_id = transaction_id
        db.commit()

        grant_access(db, payment)

        audit = PaymentAudit(payment_id=payment.id, reference=reference, event="payment_success", details="Webhook Airtel confirmé")
        db.add(audit)
        db.commit()
    elif status in ("FAILED", "rejected"):
        payment.status = "FAILED"
        payment.error_message = f"Airtel: {status}"
        db.commit()

        audit = PaymentAudit(payment_id=payment.id, reference=reference, event="payment_failed", details=f"Webhook Airtel: {status}")
        db.add(audit)
        db.commit()

    return {"status": "ok"}


@router.post("/webhook/orange")
async def webhook_orange(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    order_id = body.get("order_id", "")
    status = body.get("status", "")
    txn_id = body.get("txnid", "")

    payment = db.query(Payment).filter(Payment.reference == order_id).first()
    if not payment:
        return {"status": "error", "message": "Payment not found"}

    already_processed = db.query(PaymentAudit).filter(
        PaymentAudit.payment_id == payment.id,
        PaymentAudit.event == "payment_success",
    ).first()
    if already_processed:
        return {"status": "ok", "message": "Already processed"}

    if status == "SUCCESS":
        payment.status = "SUCCESS"
        payment.paid_at = datetime.utcnow()
        payment.provider_transaction_id = txn_id
        db.commit()

        grant_access(db, payment)

        audit = PaymentAudit(payment_id=payment.id, reference=order_id, event="payment_success", details="Webhook Orange confirmé")
        db.add(audit)
        db.commit()
    elif status in ("FAILED", "EXPIRED"):
        payment.status = "FAILED"
        payment.error_message = f"Orange: {status}"
        db.commit()

        audit = PaymentAudit(payment_id=payment.id, reference=order_id, event="payment_failed", details=f"Webhook Orange: {status}")
        db.add(audit)
        db.commit()

    return {"status": "ok"}


@router.get("/access/{student_name}/{promotion}/{level}")
def check_access(student_name: str, promotion: str, level: str, db: Session = Depends(get_db)):
    result = check_student_access(db, student_name, promotion, level)
    return result


@router.get("/history/{student_name}/{promotion}/{level}", response_model=list[PaymentHistoryItem])
def get_payment_history(student_name: str, promotion: str, level: str, db: Session = Depends(get_db)):
    payments = (
        db.query(Payment)
        .filter(
            Payment.student_name.ilike(f"%{student_name}%"),
            Payment.student_promotion == promotion,
            Payment.student_level == level,
        )
        .order_by(Payment.created_at.desc())
        .all()
    )
    return [
        PaymentHistoryItem(
            reference=p.reference,
            provider=p.provider,
            amount=p.amount,
            currency=p.currency,
            purpose=p.purpose,
            status=p.status,
            created_at=p.created_at,
            paid_at=p.paid_at,
        )
        for p in payments
    ]


@router.get("/admin/dashboard", response_model=AdminDashboardStats)
def admin_dashboard(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=now.weekday())
    month_start = today_start.replace(day=1)

    total_today = db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.created_at >= today_start, Payment.status == "SUCCESS").scalar()
    total_week = db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.created_at >= week_start, Payment.status == "SUCCESS").scalar()
    total_month = db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.created_at >= month_start, Payment.status == "SUCCESS").scalar()

    count_total = db.query(func.count(Payment.id)).scalar()
    count_success = db.query(func.count(Payment.id)).filter(Payment.status == "SUCCESS").scalar()
    count_pending = db.query(func.count(Payment.id)).filter(Payment.status == "PENDING").scalar()
    count_failed = db.query(func.count(Payment.id)).filter(Payment.status == "FAILED").scalar()

    return AdminDashboardStats(
        total_today=total_today,
        total_week=total_week,
        total_month=total_month,
        count_total=count_total,
        count_success=count_success,
        count_pending=count_pending,
        count_failed=count_failed,
    )


@router.get("/admin/payments", response_model=list[AdminPaymentRow])
def admin_list_payments(
    status: str = None,
    provider: str = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(Payment)
    if status:
        query = query.filter(Payment.status == status)
    if provider:
        query = query.filter(Payment.provider == provider)
    payments = query.order_by(Payment.created_at.desc()).limit(limit).all()
    return [
        AdminPaymentRow(
            id=p.id,
            reference=p.reference,
            student_name=p.student_name,
            provider=p.provider,
            amount=p.amount,
            currency=p.currency,
            status=p.status,
            created_at=p.created_at,
        )
        for p in payments
    ]


@router.put("/admin/config", response_model=PaymentConfigOut)
def update_config(req: UpdateConfigRequest, db: Session = Depends(get_db)):
    config = db.query(PaymentConfig).filter(PaymentConfig.key == req.key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration non trouvée")
    config.value = req.value
    db.commit()
    db.refresh(config)
    return config
