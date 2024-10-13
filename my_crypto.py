# python 
# Created by Tuan Anh Phan on 02.10.2023
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256

class newCipher:
    def __init__(self, key):
        self.BYTES_LENGTH = 16
        hash_obj = SHA256.new(key.encode()).digest()
        iv = hash_obj[:16]
        self.crypto_obj = AES.new(hash_obj, AES.MODE_CBC, iv)

    def pad(self, message: bytes):  # PKCS #5
        temp = self.BYTES_LENGTH - (len(message) % self.BYTES_LENGTH)
        return message + (bytes([temp]) * temp)

    @staticmethod
    def un_pad(message: bytes):
        return message[:-ord(message[-1:])]

    def encrypt(self, message: bytes):
        return self.crypto_obj.encrypt(self.pad(message))

    def decrypt(self, encrypted_text):
        return self.un_pad(self.crypto_obj.decrypt(encrypted_text))

    @staticmethod
    def hex_2_bytes(hex_string: str):
        return bytes.fromhex(hex_string)

    @staticmethod
    def bytes_2_hex(bytes_string: bytes):
        return bytes_string.hex()

class newHash:
    def __init__(self):
        self.pepper = b"DinhTrongMoscow"

    def hash(self, data: bytes):
        return SHA256.new(data + self.pepper).digest()

    def hash_str(self, data: str):
        return self.hash(data.encode())


def main():
    pass


if __name__ == '__main__':
    main()

