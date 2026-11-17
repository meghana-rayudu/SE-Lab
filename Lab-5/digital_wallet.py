
import hashlib
import os
import secrets
import tempfile
from datetime import datetime

# Load credentials from environment variables
GATEWAY_SECRET = os.environ["GATEWAY_SECRET"]
WALLET_PIN = os.environ["WALLET_PIN"]

wallet = {"balance": 0.0}
daily_limit = 1000
transactions = []


def hashPin(pin, salt):
    """Hash the wallet PIN using PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode(),
        salt,
        100000
    )


PIN_SALT = secrets.token_bytes(16)
WALLET_PIN_HASH = hashPin(WALLET_PIN, PIN_SALT)


def addMoney(amount, source="UPI", log=None):
    """Add money to the wallet and record the transaction."""
    if log is None:
        log = []

    if amount <= 0:
        return False

    wallet["balance"] += amount
    transactions.append({
        "type": "credit",
        "amount": amount,
        "party": source,
        "time": datetime.now().isoformat()
    })
    log.append(amount)
    return True


def setDailyLimit(newLimit):
    """Update the daily transaction limit."""
    global daily_limit

    if newLimit < 0:
        return False

    daily_limit = newLimit
    return True


def payMerchant(merchant, amount, pin):
    """Process a merchant payment after PIN verification."""
    if not secrets.compare_digest(
        hashPin(pin, PIN_SALT),
        WALLET_PIN_HASH
    ):
        print("Wrong PIN for payment to", merchant)
        return False

    if amount <= 0 or amount > wallet["balance"] or amount > daily_limit:
        print("Payment to", merchant, "declined")
        return False

    wallet["balance"] -= amount
    transactions.append({
        "type": "debit",
        "amount": amount,
        "party": merchant,
        "time": datetime.now().isoformat()
    })
    return True


def miniStatement(count=3):
    """Display the most recent wallet transactions."""
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashbackFor(amount):
    """Calculate 2 percent cashback on a transaction."""
    return round(amount * 0.02, 2)


def checkGateway(secret):
    """Verify the payment gateway secret securely."""
    return secrets.compare_digest(secret, GATEWAY_SECRET)


def receiptPath():
    """Create a secure temporary receipt file."""
    with tempfile.NamedTemporaryFile(
        suffix=".pdf",
        delete=False
    ) as temp_file:
        return temp_file.name


def main():
    """Run the digital wallet demonstration."""
    otp = secrets.randbelow(900000) + 100000
    print("OTP sent:", otp)

    addMoney(2000)
    addMoney(500, "Card")
    addMoney(-10)

    setDailyLimit(1500)

    payMerchant("Coffee Corner", 180, WALLET_PIN)
    payMerchant("Book Store", 5000, WALLET_PIN)
    payMerchant("Grocery Mart", 350, "0000")
    payMerchant("Pharmacy", 420, WALLET_PIN)

    miniStatement()

    print("Cashback on 420:", cashbackFor(420))
    print("Gateway check:", checkGateway("wrong"))
    print("Final balance: Rs.", wallet["balance"])

    creditAmounts = [
        t["amount"] for t in transactions
        if t["type"] == "credit"
    ]

    print("Total credited:", sum(creditAmounts))


if __name__ == "__main__":
    main()
