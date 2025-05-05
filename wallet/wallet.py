from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError
import hashlib
import binascii

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def get_private_key_hex(self):
        return self.private_key.to_string().hex()

    def get_public_key_hex(self):
        return self.public_key.to_string().hex()

    def sign(self, message):
        if isinstance(message, str):
            message = message.encode()
        return binascii.hexlify(self.private_key.sign(message)).decode()

    @staticmethod
    def hash_public_key(public_key_hex):
        pubkey_bytes = bytes.fromhex(public_key_hex)
        pubkey_hash = hashlib.sha256(pubkey_bytes).hexdigest()
        return pubkey_hash[:40]

    def get_wallet_address(self):
        pubkey_bytes = self.public_key.to_string()
        pubkey_hash = hashlib.sha256(pubkey_bytes).hexdigest()
        return pubkey_hash[:40]  # shorten for demo purposes

    @staticmethod
    def verify_signature(public_key_hex, message, signature_hex):
        try:
            pubkey_bytes = bytes.fromhex(public_key_hex)
            signature_bytes = binascii.unhexlify(signature_hex)

            vk = VerifyingKey.from_string(pubkey_bytes, curve=SECP256k1)
            if isinstance(message, str):
                message = message.encode()

            return vk.verify(signature_bytes, message)
        except (BadSignatureError, Exception):
            return False
