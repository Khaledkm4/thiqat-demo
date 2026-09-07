def submit_transfer(amount, recipient):
    # Demo only: intentionally missing authorization and audit controls.
    return {
        "status": "submitted",
        "amount": amount,
        "recipient": recipient,
    }
