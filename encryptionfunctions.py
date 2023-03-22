from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

def encrypt_string(string_to_encrypt: str):
    load_dotenv()
    key = os.getenv("ENCRYPTION_KEY").encode("utf-8")
    f = Fernet(key)

    if type(string_to_encrypt) == str:
        string_to_encrypt = string_to_encrypt.encode("utf-8")
    token = f.encrypt(string_to_encrypt)

    return token.decode("utf-8")


def decrypt_string(string_to_decrypt: str):
    load_dotenv()
    key = os.getenv("ENCRYPTION_KEY").encode("utf-8")
    f = Fernet(key)

    if type(string_to_decrypt) == str:
        string_to_decrypt = string_to_decrypt.encode("utf-8")
    token = f.decrypt(string_to_decrypt)

    return token.decode("utf-8")
    