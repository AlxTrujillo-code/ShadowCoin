# ShadowCoin

ShadowCoin is a simple cryptocurrency project built in Python for educational purposes. It demonstrates the core principles behind blockchain systems like Bitcoin, including wallet creation, digital signatures, mining, and basic RESTful APIs for interacting with the blockchain.

---

## Features

- Wallet creation using ECDSA (secp256k1)
- Transaction signing and verification
- Hash-linked blockchain with proof-of-work mining
- Mining rewards and balance tracking
- RESTful API for submitting transactions, mining blocks, checking balances, and viewing transaction history

---

## Project Structure

```
ShadowCoin/
├── blockchain/         # Blockchain logic
│   └── blockchain.py
├── wallet/             # Wallet key generation & signing
│   └── wallet.py
├── api/                # Flask API server
│   └── app.py
├── send_tx.py          # Script to mine and send a transaction
├── check_wallet.py     # Script to check balance and history
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
# Clone the repository
https://github.com/AlxTrujillo-code/ShadowCoin.git
cd ShadowCoin

# Create and activate virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the API Server
```bash
python api/app.py
```
This will start a Flask server at `http://localhost:5000`

---

## API Endpoints

### `POST /transaction`
Submit a signed transaction.
**Body:**
```json
{
  "from": "<sender_address>",
  "to": "<receiver_address>",
  "amount": 10,
  "public_key": "<hex_public_key>",
  "signature": "<hex_signature>"
}
```

### `POST /mine`
Mine a new block and reward the miner.
**Body:**
```json
{
  "miner_address": "<wallet_address>"
}
```

### `GET /balance/<address>`
Returns current SHDW balance of a given wallet address.

### `GET /history/<address>`
Returns transaction history of the specified address.

### `GET /chain`
Returns the full blockchain.

---

## Example Scripts

### `send_tx.py`
- Creates wallets
- Mines a block to fund the sender
- Sends a signed transaction

### `check_wallet.py`
- Displays balance and transaction history for a given address

---

## Technologies Used

- Python 3
- Flask
- ecdsa (for cryptographic keys and signing)
- requests (for testing and interacting with the API)

---

## License

This project is licensed under the MIT License.

