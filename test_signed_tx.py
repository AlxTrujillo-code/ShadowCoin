from wallet.wallet import Wallet
from blockchain.blockchain import Blockchain
import json

wallet1 = Wallet()
wallet2 = Wallet()

bc = Blockchain()

#  Wallet1 tries to send 50 SHDW — should fail (balance is 0)
msg1 = f"{wallet1.get_wallet_address()}:{wallet2.get_wallet_address()}:50"
sig1 = wallet1.sign(msg1)
tx1 = {
    'from': wallet1.get_wallet_address(),
    'to': wallet2.get_wallet_address(),
    'amount': 50,
    'public_key': wallet1.get_public_key_hex(),
    'signature': sig1
}
bc.add_transaction(tx1)

# Mine a reward to wallet1
bc.mine_pending_transactions(wallet1.get_wallet_address())

# Wallet1 now sends 10 SHDW — should succeed
msg2 = f"{wallet1.get_wallet_address()}:{wallet2.get_wallet_address()}:10"
sig2 = wallet1.sign(msg2)
tx2 = {
    'from': wallet1.get_wallet_address(),
    'to': wallet2.get_wallet_address(),
    'amount': 10,
    'public_key': wallet1.get_public_key_hex(),
    'signature': sig2
}
bc.add_transaction(tx2)
bc.mine_pending_transactions(wallet1.get_wallet_address())

#  Check balances
print("Wallet1 balance:", bc.get_balance(wallet1.get_wallet_address()))
print("Wallet2 balance:", bc.get_balance(wallet2.get_wallet_address()))


print("\nWallet1 History:")
for tx in bc.get_transaction_history(wallet1.get_wallet_address()):
    print(json.dumps(tx, indent=2))

print("\nWallet2 History:")
for tx in bc.get_transaction_history(wallet2.get_wallet_address()):
    print(json.dumps(tx, indent=2))

