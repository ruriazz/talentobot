import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from common.settings import SECRET_KEY
from libs import strings


class TextEncryption:
    def __init__(self, password: str = ''):
        """Initialize the helper with a password or passphrase."""
        self.password = strings.shuffle_texts(SECRET_KEY, password)

    def _generate_key(self, salt: bytes) -> bytes:
        """
        Generate a 256-bit key using Scrypt key derivation function.
        :param salt: Randomly generated salt
        :return: 256-bit encryption key
        """
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )
        return kdf.derive(self.password.encode())

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt the given plaintext using AES encryption (CBC mode).
        :param plaintext: The data to be encrypted
        :return: Base64 encoded string of the encrypted data
        """
        salt = os.urandom(16)
        key = self._generate_key(salt)
        iv = os.urandom(16)

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return base64.b64encode(salt + iv + ciphertext).decode('utf-8')

    def decrypt(self, ciphertext_b64: str) -> str:
        """
        Decrypt the given Base64 encoded ciphertext using AES decryption (CBC mode).
        :param ciphertext_b64: Base64 encoded encrypted data
        :return: The original plaintext
        """
        ciphertext = base64.b64decode(ciphertext_b64)

        salt = ciphertext[:16]
        iv = ciphertext[16:32]
        actual_ciphertext = ciphertext[32:]

        key = self._generate_key(salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext.decode('utf-8')