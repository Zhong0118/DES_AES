from Crypto.Cipher import AES, DES
from hashlib import pbkdf2_hmac


def get_des_key(key):
    return pbkdf2_hmac("sha256", key.encode("utf-8"), b"salt", 10000, dklen=8)

def get_aes_key(key):
    return pbkdf2_hmac("sha256", key.encode("utf-8"), b"salt", 10000, dklen=16)

def des_encrypt(data, key):
    key = get_des_key(key)
    data_bytes = data.encode()
    if len(data_bytes) % 8 != 0:
            padding_length = 8 - (len(data_bytes) % 8)
            data_bytes += bytes([padding_length] * padding_length)
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted = cipher.encrypt(data_bytes)
    return encrypted

def des_decrypt(encrypted_data, key):
    key = get_des_key(key)
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted = cipher.decrypt(encrypted_data)
    padding_length = decrypted[-1]
    return decrypted[:-padding_length]


def aes_encrypt(data, key):
    key = get_aes_key(key)
    data_bytes = data.encode()
    if len(data_bytes) % 16 != 0:
        padding_length = 16 - (len(data_bytes) % 16)
        data_bytes += bytes([padding_length] * padding_length)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(data_bytes)
    return encrypted

def aes_decrypt(encrypted_data, key):
    key = get_aes_key(key)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(encrypted_data)
    padding_length = decrypted[-1]
    return decrypted[:-padding_length]
