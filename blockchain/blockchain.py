from wallet.wallet import Wallet
import time
import hashlib
import json

BLOCK_REWARD = 10
COIN_NAME = "ShadowCoin"
COIN_SYMBOL = "SHDW"

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self):
        return f"Block<{self.index}, {self.hash[:10]}...>"


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, time.time(), ["Genesis Block"], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        required_keys = ['from', 'to', 'amount', 'public_key', 'signature']

        if not all(k in transaction for k in required_keys):
            print("Invalid transaction format.")
            return False

        message = f"{transaction['from']}:{transaction['to']}:{transaction['amount']}"

#debugging - showing everything is being verified
        print("\n🔍 Verifying Transaction:")
        print("→ Signed Message:", message)
        print("→ Public Key:", transaction['public_key'])
        print("→ Signature:", transaction['signature'])


        is_valid = Wallet.verify_signature(
            transaction['public_key'],
            message,
            transaction['signature']
        )

        print("→ Signature Valid?", is_valid)

        derived_address = Wallet.hash_public_key(transaction['public_key'])
        print("→ Derived Address from Public Key:", derived_address)
        print("→ Claimed Sender Address:", transaction['from'])

        if not is_valid:
            print("Signature verification failed.")
            return False
        if derived_address != transaction['from']:
            print("Public key does not match sender address.")
            return False

        sender_balance = self.get_balance(transaction['from'])

        if transaction['amount'] > sender_balance:
            print(f"insufficient funds. Balance: {sender_balance}, attempted: {transaction['amount']}")
            return False

        self.pending_transactions.append(transaction)
        print("Transaction added to pool.")
        return True

    def mine_pending_transactions(self, miner_address):
        self.pending_transactions.append({
            'from': 'network',
            'to': miner_address,
            'amount': BLOCK_REWARD
        })

        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )

        self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.pending_transactions = []

    def proof_of_work(self, block):
        print(f"Mining block {block.index}...")
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        print(f"Block mined: {block.hash}")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def get_balance(self, address):
        balance = 0

        for block in self.chain:
            for tx in block.transactions:
                if not isinstance(tx, dict):
                    continue
                if 'from' not in tx or 'to' not in tx or 'amount' not in tx:
                    continue

                if tx['from'] == address:
                    balance -= tx['amount']
                if tx['to'] == address:
                    balance += tx['amount']

        for tx in self.pending_transactions:
            if not isinstance(tx, dict):
                continue
            if 'from' not in tx or 'to' not in tx or 'amount' not in tx:
                continue

            if tx['from'] == address:
                balance -= tx['amount']
            if tx['to'] == address:
                balance += tx['amount']

        return balance

    def get_transaction_history(self, address):
        history = []

        # Search mined blocks
        for block in self.chain:
            for tx in block.transactions:
                if not isinstance(tx, dict):
                    continue
                if tx.get('from') == address or tx.get('to') == address:
                    history.append(tx)

        # Also include pending transactions
        for tx in self.pending_transactions:
            if not isinstance(tx, dict):
                continue
            if tx.get('from') == address or tx.get('to') == address:
                history.append(tx)

        return history
