import uuid
import logging

logging.basicConfig(level=logging.INFO)

# Current business rule (Legacy limit: 25,000 SAR)
MAX_TRANSFER_LIMIT_SAR = 25000

def process_transfer(customer_id: str, amount: float, is_authorized: bool) -> dict:
    # Generate transaction identifier early for auditability of all requests
    tx_id = str(uuid.uuid4())

    # 1. Validate authorization and record audit event
    auth_status = "AUTHORIZED" if is_authorized else "UNAUTHORIZED"
    logging.info(f"AUDIT_EVENT | TxID={tx_id} | Customer={customer_id} | AuthorizationResult={auth_status}")

    if not is_authorized:
        raise PermissionError("Transfer rejected: Customer authorization required.")

    # 2. Reject non-positive amounts
    if amount <= 0:
        logging.warning(f"AUDIT_EVENT | TxID={tx_id} | Customer={customer_id} | Amount={amount} SAR | Status=REJECTED | Reason=NonPositiveAmount")
        raise ValueError("Transfer rejected: Amount must be strictly positive.")

    # 3. Check transfer limit
    if amount > MAX_TRANSFER_LIMIT_SAR:
        logging.warning(f"AUDIT_EVENT | TxID={tx_id} | Customer={customer_id} | Amount={amount} SAR | Status=REJECTED | Reason=ExceedsLimit")
        raise ValueError(f"Transfer rejected: Amount exceeds maximum limit of {MAX_TRANSFER_LIMIT_SAR} SAR.")

    # Final success audit log
    logging.info(f"AUDIT_EVENT | TxID={tx_id} | Customer={customer_id} | Amount={amount} SAR | Status=APPROVED")

    return {
        "status": "APPROVED",
        "transaction_id": tx_id,
        "amount": amount
    }