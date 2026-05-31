"""AGENTIK Security — Receipts HMAC para verificación criptográfica."""

import hashlib
import hmac
import json
import uuid
from datetime import datetime


def generate_receipt(action: str, result: str, secret_key: str = "agentik-default-key") -> dict:
    """Generate an HMAC receipt for an action."""
    receipt = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "actor": "agentik",
        "result": result
    }

    # Create HMAC signature
    message = json.dumps(receipt, sort_keys=True).encode()
    signature = hmac.new(
        secret_key.encode(),
        message,
        hashlib.sha256
    ).hexdigest()

    receipt["signature"] = signature
    return receipt


def verify_receipt(receipt: dict, secret_key: str = "agentik-default-key") -> bool:
    """Verify the HMAC signature of a receipt."""
    if "signature" not in receipt:
        return False

    stored_signature = receipt.pop("signature")
    message = json.dumps(receipt, sort_keys=True).encode()
    expected_signature = hmac.new(
        secret_key.encode(),
        message,
        hashlib.sha256
    ).hexdigest()

    receipt["signature"] = stored_signature
    return hmac.compare_digest(stored_signature, expected_signature)
