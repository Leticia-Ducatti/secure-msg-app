from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

# ---------- AES Encryption / Decryption (Symmetric) ----------

def generate_aes_key():
    return get_random_bytes(16)

def encrypt_aes(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return {
        'cipher_text': base64.b64encode(ciphertext).decode(),
        'nonce': base64.b64encode(cipher.nonce).decode(),
        'tag': base64.b64encode(tag).decode()
    }

def decrypt_aes(encrypted, key):
    nonce = base64.b64decode(encrypted['nonce'])
    ciphertext = base64.b64decode(encrypted['cipher_text'])
    tag = base64.b64decode(encrypted['tag'])
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# ---------- RSA Key Generation / Encryption / Decryption ----------

def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_rsa(message, public_key_bytes):
    public_key = RSA.import_key(public_key_bytes)
    cipher = PKCS1_OAEP.new(public_key)
    return base64.b64encode(cipher.encrypt(message.encode())).decode()

def decrypt_rsa(cipher_text_b64, private_key_bytes):
    private_key = RSA.import_key(private_key_bytes)
    cipher = PKCS1_OAEP.new(private_key)
    cipher_text = base64.b64decode(cipher_text_b64)
    return cipher.decrypt(cipher_text).decode()
