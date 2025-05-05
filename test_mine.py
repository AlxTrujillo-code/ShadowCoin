from blockchain.blockchain import Blockchain

# Create blockchain instance
shadowcoin = Blockchain()

# Add a test transaction
shadowcoin.add_transaction({'from': 'alejandro', 'to': 'wallet2', 'amount': 25})

# Mine a new block
shadowcoin.mine_pending_transactions('miner_wallet')

# Print the full chain
for block in shadowcoin.chain:
    print(block)
