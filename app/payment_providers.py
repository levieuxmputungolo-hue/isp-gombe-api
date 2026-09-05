import os
import time
import hashlib
import hmac
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class PaymentResult:
    def __init__(self, success: bool, transaction_id: str = "", message: str = "", raw_response: dict = None):
        self.success = success
        self.transaction_id = transaction_id
        self.message = message
        self.raw_response = raw_response or {}


class PaymentProvider(ABC):
    @abstractmethod
    def initiate_payment(self, reference: str, phone_number: str, amount: float, currency: str) -> PaymentResult:
        pass

    @abstractmethod
    def check_status(self, reference: str, transaction_id: str = "") -> PaymentResult:
        pass

    @abstractmethod
    def verify_callback(self, payload: dict, signature: str = "") -> bool:
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        pass


class MpesaProvider(PaymentProvider):
    def __init__(self):
        self.api_key = os.getenv("MPESA_API_KEY", "")
        self.secret = os.getenv("MPESA_SECRET", "")
        self.base_url = os.getenv("MPESA_BASE_URL", "https://sandbox.safaricom.co.ke")
        self.short_code = os.getenv("MPESA_SHORT_CODE", "")
        self.passkey = os.getenv("MPESA_PASSKEY", "")
        self.test_mode = not bool(self.api_key)

    def get_provider_name(self) -> str:
        return "MPESA"

    def initiate_payment(self, reference: str, phone_number: str, amount: float, currency: str) -> PaymentResult:
        if self.test_mode:
            return PaymentResult(
                success=True,
                transaction_id=f"MPESA-TEST-{reference}",
                message="Paiement initié en mode TEST. En attente de confirmation.",
            )

        try:
            import httpx
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = f"{self.short_code}{self.passkey}{timestamp}"
            encoded_password = __import__("base64").b64encode(password.encode()).decode()

            token_resp = httpx.get(
                f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
                auth=(self.api_key, self.secret),
                timeout=30,
            )
            access_token = token_resp.json().get("access_token", "")

            payload = {
                "BusinessShortCode": self.short_code,
                "Password": encoded_password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone_number,
                "PartyB": self.short_code,
                "PhoneNumber": phone_number,
                "CallBackURL": f"{os.getenv('BASE_URL', 'http://localhost:8003')}/api/payments/webhook/mpesa",
                "AccountReference": reference,
                "TransactionDesc": f"Paiement résultats - {reference}",
            }

            resp = httpx.post(
                f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=30,
            )

            data = resp.json()
            if data.get("ResponseCode") == "0":
                return PaymentResult(
                    success=True,
                    transaction_id=data.get("CheckoutRequestID", ""),
                    message="STK Push envoyé. En attente de confirmation.",
                    raw_response=data,
                )
            else:
                return PaymentResult(
                    success=False,
                    message=data.get("errorMessage", "Erreur lors de l'initiation du paiement"),
                    raw_response=data,
                )
        except Exception as e:
            return PaymentResult(success=False, message=f"Erreur réseau: {str(e)}")

    def check_status(self, reference: str, transaction_id: str = "") -> PaymentResult:
        if self.test_mode:
            return PaymentResult(
                success=True,
                transaction_id=transaction_id,
                message="Mode TEST: paiement considéré comme réussi après 5 secondes.",
            )

        try:
            import httpx
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = f"{self.short_code}{self.passkey}{timestamp}"
            encoded_password = __import__("base64").b64encode(password.encode()).decode()

            token_resp = httpx.get(
                f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
                auth=(self.api_key, self.secret),
                timeout=30,
            )
            access_token = token_resp.json().get("access_token", "")

            resp = httpx.post(
                f"{self.base_url}/mpesa/transactionstatus/v1/query",
                json={
                    "Initiator": self.short_code,
                    "SecurityCredential": encoded_password,
                    "CommandID": "TransactionStatusQuery",
                    "TransactionID": transaction_id,
                    "OriginatorConversationID": reference,
                    "ResultURL": f"{os.getenv('BASE_URL', 'http://localhost:8003')}/api/payments/webhook/mpesa",
                },
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=30,
            )

            data = resp.json()
            result_code = data.get("ResultCode", "")
            if result_code == "0":
                return PaymentResult(success=True, transaction_id=transaction_id, message="Transaction confirmée")
            elif result_code in ("1032", "1037"):
                return PaymentResult(success=False, transaction_id=transaction_id, message="Transaction en cours ou annulée")
            else:
                return PaymentResult(success=False, transaction_id=transaction_id, message=f"Code: {result_code}")
        except Exception as e:
            return PaymentResult(success=False, message=f"Erreur: {str(e)}")

    def verify_callback(self, payload: dict, signature: str = "") -> bool:
        if self.test_mode:
            return True

        try:
            stk_callback = payload.get("Body", {}).get("stkCallback", {})
            merchant_request_id = stk_callback.get("MerchantRequestID", "")
            checkout_request_id = stk_callback.get("CheckoutRequestID", "")
            result_code = stk_callback.get("ResultCode", -1)

            expected_sig = hmac.new(
                self.secret.encode(),
                f"{merchant_request_id}{checkout_request_id}".encode(),
                hashlib.sha256,
            ).hexdigest()

            return hmac.compare_digest(expected_sig, signature)
        except Exception:
            return False


class AirtelMoneyProvider(PaymentProvider):
    def __init__(self):
        self.client_id = os.getenv("AIRTEL_CLIENT_ID", "")
        self.client_secret = os.getenv("AIRTEL_CLIENT_SECRET", "")
        self.base_url = os.getenv("AIRTEL_BASE_URL", "https://sandbox.airtel.africa")
        self.country = os.getenv("AIRTEL_COUNTRY", "CD")
        self.test_mode = not bool(self.client_id)

    def get_provider_name(self) -> str:
        return "AIRTEL_MONEY"

    def initiate_payment(self, reference: str, phone_number: str, amount: float, currency: str) -> PaymentResult:
        if self.test_mode:
            return PaymentResult(
                success=True,
                transaction_id=f"AIRTEL-TEST-{reference}",
                message="Paiement initié en mode TEST. En attente de confirmation.",
            )

        try:
            import httpx

            token_resp = httpx.post(
                f"{self.base_url}/auth/oauth/token",
                data={"client_id": self.client_id, "client_secret": self.client_secret, "grant_type": "client_credentials"},
                timeout=30,
            )
            access_token = token_resp.json().get("access_token", "")

            payload = {
                "reference": reference,
                "subscriber": {"country": self.country, "msisdn": phone_number},
                "transaction": {
                    "amount": amount,
                    "country": self.country,
                    "currency": currency,
                    "reference": reference,
                },
            }

            resp = httpx.post(
                f"{self.base_url}/merchant/v1/payments/",
                json=payload,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "X-Country": self.country,
                    "X-Currency": currency,
                },
                timeout=30,
            )

            data = resp.json()
            if data.get("status", {}).get("code") == 200:
                txn_id = data.get("data", {}).get("transaction", {}).get("id", "")
                return PaymentResult(success=True, transaction_id=txn_id, message="Paiement initié", raw_response=data)
            else:
                return PaymentResult(success=False, message=data.get("status", {}).get("message", "Erreur"), raw_response=data)
        except Exception as e:
            return PaymentResult(success=False, message=f"Erreur réseau: {str(e)}")

    def check_status(self, reference: str, transaction_id: str = "") -> PaymentResult:
        if self.test_mode:
            return PaymentResult(success=True, transaction_id=transaction_id, message="Mode TEST: succès simulé")

        try:
            import httpx

            token_resp = httpx.post(
                f"{self.base_url}/auth/oauth/token",
                data={"client_id": self.client_id, "client_secret": self.client_secret, "grant_type": "client_credentials"},
                timeout=30,
            )
            access_token = token_resp.json().get("access_token", "")

            resp = httpx.get(
                f"{self.base_url}/transaction/v1/{transaction_id}",
                headers={"Authorization": f"Bearer {access_token}", "X-Country": self.country},
                timeout=30,
            )

            data = resp.json()
            status = data.get("data", {}).get("status", "")
            if status in ("SUCCESSFUL", "completed"):
                return PaymentResult(success=True, transaction_id=transaction_id, message="Confirmé")
            elif status in ("FAILED", "rejected"):
                return PaymentResult(success=False, transaction_id=transaction_id, message="Échoué")
            else:
                return PaymentResult(success=False, transaction_id=transaction_id, message="En attente")
        except Exception as e:
            return PaymentResult(success=False, message=f"Erreur: {str(e)}")

    def verify_callback(self, payload: dict, signature: str = "") -> bool:
        if self.test_mode:
            return True
        return True


class OrangeMoneyProvider(PaymentProvider):
    def __init__(self):
        self.client_id = os.getenv("ORANGE_CLIENT_ID", "")
        self.client_secret = os.getenv("ORANGE_CLIENT_SECRET", "")
        self.merchant_key = os.getenv("ORANGE_MERCHANT_KEY", "")
        self.base_url = os.getenv("ORANGE_BASE_URL", "https://api.orange.com")
        self.country = os.getenv("ORANGE_COUNTRY", "CD")
        self.test_mode = not bool(self.client_id)

    def get_provider_name(self) -> str:
        return "ORANGE_MONEY"

    def initiate_payment(self, reference: str, phone_number: str, amount: float, currency: str) -> PaymentResult:
        if self.test_mode:
            return PaymentResult(
                success=True,
                transaction_id=f"ORANGE-TEST-{reference}",
                message="Paiement initié en mode TEST. En attente de confirmation.",
            )

        try:
            import httpx

            token_resp = httpx.post(
                f"{self.base_url}/oauth/v3/token",
                data={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
                timeout=30,
            )
            access_token = token_resp.json().get("access_token", "")

            payload = {
                "merchant_key": self.merchant_key,
                "currency": currency,
                "order_id": reference,
                "amount": amount,
                "return_url": f"{os.getenv('BASE_URL', 'http://localhost:8003')}/api/payments/webhook/orange",
                "cancel_url": f"{os.getenv('BASE_URL', 'http://localhost:8003')}/api/payments/webhook/orange",
                "notif_url": f"{os.getenv('BASE_URL', 'http://localhost:8003')}/api/payments/webhook/orange",
                "lang": "fr",
            }

            resp = httpx.post(
                f"{self.base_url}/orange-money-webpay/dev/v1/webpayment",
                json=payload,
                headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
                timeout=30,
            )

            data = resp.json()
            if data.get("status") == 201 or data.get("payment_url"):
                pay_token = data.get("pay_token", "")
                return PaymentResult(success=True, transaction_id=pay_token, message="Paiement initié", raw_response=data)
            else:
                return PaymentResult(success=False, message=data.get("message", "Erreur"), raw_response=data)
        except Exception as e:
            return PaymentResult(success=False, message=f"Erreur réseau: {str(e)}")

    def check_status(self, reference: str, transaction_id: str = "") -> PaymentResult:
        if self.test_mode:
            return PaymentResult(success=True, transaction_id=transaction_id, message="Mode TEST: succès simulé")

        try:
            import httpx

            token_resp = httpx.post(
                f"{self.base_url}/oauth/v3/token",
                data={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
                timeout=30,
            )
            access_token = token_resp.json().get("access_token", "")

            resp = httpx.get(
                f"{self.base_url}/orange-money-webpay/dev/v1/transactionstatus/{reference}",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=30,
            )

            data = resp.json()
            status = data.get("status", "")
            if status == "SUCCESS":
                return PaymentResult(success=True, transaction_id=transaction_id, message="Confirmé")
            elif status in ("FAILED", "EXPIRED"):
                return PaymentResult(success=False, transaction_id=transaction_id, message=status)
            else:
                return PaymentResult(success=False, transaction_id=transaction_id, message="En attente")
        except Exception as e:
            return PaymentResult(success=False, message=f"Erreur: {str(e)}")

    def verify_callback(self, payload: dict, signature: str = "") -> bool:
        if self.test_mode:
            return True
        return True


def get_provider(provider_name: str) -> PaymentProvider:
    providers = {
        "MPESA": MpesaProvider,
        "AIRTEL_MONEY": AirtelMoneyProvider,
        "ORANGE_MONEY": OrangeMoneyProvider,
    }
    provider_class = providers.get(provider_name)
    if not provider_class:
        raise ValueError(f"Fournisseur inconnu: {provider_name}")
    return provider_class()


def get_all_providers_status() -> dict:
    return {
        "MPESA": {"enabled": True, "test_mode": MpesaProvider().test_mode},
        "AIRTEL_MONEY": {"enabled": True, "test_mode": AirtelMoneyProvider().test_mode},
        "ORANGE_MONEY": {"enabled": True, "test_mode": OrangeMoneyProvider().test_mode},
    }
