from cryptography.fernet import Fernet

FERNET_KEY = Fernet.generate_key()
cipher = Fernet(FERNET_KEY)

def encrypt_text(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(enc_text):
    return cipher.decrypt(enc_text.encode()).decode()
