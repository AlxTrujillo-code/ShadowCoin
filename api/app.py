import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request
from blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route("/chain", methods=["GET"])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify(chain_data), 200

@app.route("/balance/<address>", methods=["GET"])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({"address": address, "balance": balance}), 200

@app.route("/history/<address>", methods=["GET"])
def get_history(address):
    history = blockchain.get_transaction_history(address)
    return jsonify(history), 200

@app.route("/transaction", methods=["POST"])
def add_transaction():
    data = request.get_json()
    if blockchain.add_transaction(data):
        return jsonify({"message": "Transaction added."}), 201
    return jsonify({"message": "Invalid transaction."}), 400

@app.route("/mine", methods=["POST"])
def mine_block():
    data = request.get_json()
    if not data or "miner_address" not in data:
        return jsonify({"message": "Missing miner address."}), 400

    blockchain.mine_pending_transactions(data["miner_address"])
    return jsonify({"message": "Block mined."}), 201

if __name__ == "__main__":
    app.run(port=5000)
