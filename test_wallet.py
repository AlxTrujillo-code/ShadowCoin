from wallet.wallet import Wallet

wallet1 = Wallet()
wallet2 = Wallet()

message = "Send 10 SHDW to bob"
signature = wallet1.sign(message)

print("Signature:", signature)
print("Wallet1 Verified:", Wallet.verify_signature(wallet1.get_public_key_hex(), message, signature))
print("Wallet2 Verified:", Wallet.verify_signature(wallet2.get_public_key_hex(), message, signature))
