import requests

# Replace this with the address you want to check
wallet_address = "f4f7ec65584a7397830a351c09b4b6b56417f7f3"

# 1. Get Balance
balance_response = requests.get(f"http://localhost:5000/balance/{wallet_address}")
balance = balance_response.json()
print(f" Balance for {wallet_address}: {balance['balance']} SHDW")

# 2. Get Transaction History
history_response = requests.get(f"http://localhost:5000/history/{wallet_address}")
history = history_response.json()

print(f"\n Transaction History for {wallet_address}:")
if history:
    for tx in history:
        print(tx)
else:
    print("No transactions found.")
