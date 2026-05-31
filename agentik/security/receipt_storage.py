"""AGENTIK Receipt Storage — Store and retrieve receipts."""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from agentik.security.receipts import generate_receipt, verify_receipt


class ReceiptStorage:
    """Store and retrieve receipts locally."""
    
    def __init__(self, storage_dir: str = "~/.agentik/receipts"):
        self.storage_dir = os.path.expanduser(storage_dir)
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def store_receipt(self, receipt: Dict) -> bool:
        """Store a receipt to file."""
        try:
            filepath = os.path.join(self.storage_dir, f"{receipt['id']}.json")
            with open(filepath, 'w') as f:
                json.dump(receipt, f, indent=2)
            return True
        except Exception as e:
            print(f"Error storing receipt: {e}")
            return False
    
    def create_and_store(self, action: str, result: str, secret_key: str = "agentik-default-key") -> Dict:
        """Create a receipt and store it."""
        receipt = generate_receipt(action, result, secret_key)
        self.store_receipt(receipt)
        return receipt
    
    def retrieve(self, receipt_id: str, secret_key: str = "agentik-default-key") -> Optional[Dict]:
        """Retrieve and verify a receipt."""
        try:
            filepath = os.path.join(self.storage_dir, f"{receipt_id}.json")
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    receipt = json.load(f)
                if verify_receipt(receipt, secret_key):
                    return receipt
            return None
        except Exception as e:
            print(f"Error retrieving receipt: {e}")
            return None
    
    def list_receipts(self, count: int = 10) -> List[Dict]:
        """List recent receipts."""
        try:
            files = [f for f in os.listdir(self.storage_dir) if f.endswith('.json')]
            files.sort(reverse=True)
            receipts = []
            for file in files[:count]:
                filepath = os.path.join(self.storage_dir, file)
                with open(filepath, 'r') as f:
                    receipts.append(json.load(f))
            return receipts
        except Exception as e:
            print(f"Error listing receipts: {e}")
            return []
    
    def get_receipt_count(self) -> int:
        """Get total number of receipts."""
        try:
            return len([f for f in os.listdir(self.storage_dir) if f.endswith('.json')])
        except Exception:
            return 0


# Global receipt storage instance
receipt_storage = ReceiptStorage()
