from wallet.wallet import Wallet
import requests
import time

# Step 1: Setup wallets
sender = Wallet()
receiver = Wallet()

sender_address = sender.get_wallet_address()
receiver_address = receiver.get_wallet_address()

miner_address = sender.get_wallet_address()

mine_response = requests.post(
    "http://localhost:5000/mine",
    json={"miner_address": sender_address}
)
print("🪙 Mine Response:", mine_response.status_code, mine_response.json())

#added a time delay to let reward take effect
time.sleep(1)

balance_response = requests.get(f"http://localhost:5000/balance/{sender_address}")
print("💰 Sender Balance:", balance_response.json())

# Step 2: Sign the message
amount = 10
message = f"{sender.get_wallet_address()}:{receiver.get_wallet_address()}:{amount}"
signature = sender.sign(message)

# Step 3: Build the transaction object
tx = {
    "from": sender.get_wallet_address(),
    "to": receiver.get_wallet_address(),
    "amount": amount,
    "public_key": sender.get_public_key_hex(),
    "signature": signature
}

# Step 4: Submit transaction to Flask API
response = requests.post("http://localhost:5000/transaction", json=tx)
print("Response Code:", response.status_code)
print("Response JSON:", response.json())

# Optional: Print addresses to check later
print("\nSender Address:", sender.get_wallet_address())
print("Receiver Address:", receiver.get_wallet_address())
