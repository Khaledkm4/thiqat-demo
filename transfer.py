import uuid
import logging

logging.basicConfig(level=logging.INFO)

# Current business rule (Legacy limit: 25,000 SAR)
MAX_TRANSFER_LIMIT_SAR = 25000

def process_transfer(customer_id: str, amount: float, is_authorized: bool) -> dict:
    # 1. Validate authorization
    if not is_authorized:
        raise PermissionError("Transfer rejected: Customer authorization required.")

    # 2. Reject non-positive amounts
    if amount <= 0:
        raise ValueError("Transfer rejected: Amount must be strictly positive.")

    # 3. Check transfer limit
    if amount > MAX_TRANSFER_LIMIT_SAR:
        raise ValueError(f"Transfer rejected: Amount exceeds maximum limit of {MAX_TRANSFER_LIMIT_SAR} SAR.")

    # 4. Generate transaction identifier
    tx_id = str(uuid.uuid4())

    # 5. Record immutable audit log
    logging.info(f"AUDIT_EVENT | TxID={tx_id} | Customer={customer_id} | Amount={amount} SAR | Status=SUCCESS")

    return {
        "status": "APPROVED",
        "transaction_id": tx_id,
        "amount": amount
    }
