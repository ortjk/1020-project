# 1.1
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# 1.2
def encrypt_string(string_to_encrypt: str) -> str:
    """Encrypts a string.

        Arguments:
            string_to_encrypt (str): String to encrypt.

        Returns:
            An encrypted string.
    """
    # get the encryption key from the .env file
    load_dotenv()
    key = os.getenv("ENCRYPTION_KEY").encode("utf-8")
    f = Fernet(key)

    # make sure the string is in bits
    if type(string_to_encrypt) == str:
        string_to_encrypt = string_to_encrypt.encode("utf-8")
    token = f.encrypt(string_to_encrypt)

    return token.decode("utf-8")


# 1.3
def decrypt_string(string_to_decrypt: str):
    """Decrypts a string.

        Arguments:
            string_to_encrypt (str): String to decrypt.

        Returns:
            A decrypted string.
    """
    # get the encryption key from the .env file
    load_dotenv()
    key = os.getenv("ENCRYPTION_KEY").encode("utf-8")
    f = Fernet(key)

    # make sure the string is in bits
    if type(string_to_decrypt) == str:
        string_to_decrypt = string_to_decrypt.encode("utf-8")
    token = f.decrypt(string_to_decrypt)

    return token.decode("utf-8")
    