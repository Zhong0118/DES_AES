import base64
from hashlib import pbkdf2_hmac

from des_table import *


# PKCS7 padding
def pkcs7_padding(data, block_size=64):
    pad_len = block_size - (len(data) % block_size)
    return data + chr(pad_len) * pad_len


# PKCS7 remove padding
def pkcs7_unpadding(data):
    pad_len = ord(data[-1])
    return data[:-pad_len]


# Convert the string to binary (using Base64 encoding to avoid truncation of Chinese characters)
def str2bin(s):
    base64_bytes = base64.b64encode(s.encode("utf-8"))  # the Base64 bytes after string
    return "".join(format(byte, "08b") for byte in base64_bytes)  # bytes to binary


# Convert the binary to string
def bin2str(b):
    bytes_list = [
        b[i : i + 8] for i in range(0, len(b), 8)
    ]  # binary into groups every 8 bits to get bytes list
    bytes_obj = bytes([int(byte, 2) for byte in bytes_list])  # lists to byte
    try:
        return base64.b64decode(bytes_obj).decode("utf-8")
    except (UnicodeDecodeError, base64.binascii.Error) as e:
        print(f"Failing: {e}")  # when key is wrong, it will show
        return


# Convert the binary to hexadecimal
def bin2hex(bin_str):
    return "".join(
        hex(int(bin_str[i : i + 4], 2))[2:] for i in range(0, len(bin_str), 4)
    )


# Convert the hexadecimal to binary
def hex2bin(hex_str):
    return "".join(format(int(char, 16), "04b") for char in hex_str)


# Convert the byte to binary
def byte2bin(byte_str):
    return "".join(format(byte, "08b") for byte in byte_str)


"""
the functions of getting all sub-keys
"""


# get 56 bit key
def process_key(k):
    k_hex = pbkdf2_hmac("sha256", k.encode("utf-8"), b"salt", 10000, dklen=8)
    k_str = byte2bin(k_hex)
    key_bin56 = ""
    for i in PC1_TABLE:
        key_bin56 += k_str[i - 1]
    return key_bin56


# left-loop moving
def left_turn(my_str, num):
    return my_str[num:] + my_str[:num]


# get all 16 sub-keys
def generate_keys(k):
    keys = []
    key_bin56 = process_key(k)
    c = key_bin56[0:28]
    d = key_bin56[28:]
    for i in MOVE_TABLE:
        c = left_turn(c, i)
        d = left_turn(d, i)
        total_k = c + d
        sub_key = ""
        for j in PC2_TABLE:
            sub_key += total_k[j - 1]
        keys.append(sub_key)
    return keys


"""
the process of get Ciphertext
"""


def divide(bin_str):
    # justify to group by 64 bits, whether padding '0'
    length = len(bin_str)
    if length % 64 != 0:
        bin_str += "0" * (64 - (length % 64))
    result = [bin_str[i : i + 64] for i in range(0, len(bin_str), 64)]
    return result


# permutation IP_TABLE IP2_TABLE E_TABLE P_TABLE
def trans(str_bit, table):
    result = ""
    for i in table:
        result += str_bit[i - 1]
    return result


def xor(str1, str2):
    result = ""
    for c1, c2 in zip(str1, str2):
        result += str(int(c1) ^ int(c2))
    return result


# single S table operation to get 4 bit data
def single_s(str_bit, i):
    row = int(str_bit[0] + str_bit[5], 2)
    col = int(str_bit[1:5], 2)
    num = S_BOX[i][row][col]
    return bin(num)[2:].zfill(4)


# the whole S operation in 8 loop
def s_box(str_bit):
    result = ""
    for i in range(8):
        result += single_s(str_bit[i * 6 : i * 6 + 6], i)
    return result


# whole F function
def F(str_bit, k):
    # expansion E
    str_bit = trans(str_bit, E_TABLE)
    # XORed by sub-key
    str_bit = xor(str_bit, k)
    # S operation
    str_bit = s_box(str_bit)
    # P permutation
    str_bit = trans(str_bit, P_TABLE)
    return str_bit


# encryption process
def encrypt(origin_str, k):
    # the original key to hash
    # avoid the problem of length
    # key_hash = hashlib.sha256(k.encode()).hexdigest()
    keys = generate_keys(k)
    # origin_str = pkcs7_padding(origin_str)
    bin_str = str2bin(origin_str)
    str_list = divide(bin_str)
    result = ""
    for i in str_list:
        # IP permutation
        i = trans(i, IP_TABLE)
        L, R = i[0:32], i[32:]
        # 16 looping
        for j in range(16):
            L, R = R, xor(L, F(R, keys[j]))
        # IP verse
        i = trans(R + L, IP2_TABLE)
        result += i
    return result


# decryption process
def decrypt(origin_str, k):
    # get ciphertext and hash-key
    # ciphertext = origin_str[:-256]
    # key_hash = origin_str[-256:]
    # # validate
    # if hashlib.sha256(k.encode()).hexdigest() != bin2hex(key_hash):
    #     return
    keys = generate_keys(k)
    str_list = divide(origin_str)
    result = ""
    for i in str_list:
        i = trans(i, IP_TABLE)
        L, R = i[0:32], i[32:]
        for j in range(16):
            L, R = R, xor(L, F(R, keys[15 - j]))
        i = trans(R + L, IP2_TABLE)
        result += i
    # remove padding
    result = result.rstrip("0")
    return bin2str(result)


# VALIDATION_STRING = "VALID_KEY"
# def encrypt(origin_str, k):
#     origin_str = VALIDATION_STRING + origin_str
#     keys = generate_keys(k)
#     bin_str = str2bin(origin_str)
#     str_list = divide(bin_str)
#     result = ""
#     for i in str_list:
#         i = trans(i, IP_TABLE)
#         L, R = i[0:32], i[32:]
#         for j in range(16):
#             L, R = R, xor(L, F(R, keys[j]))
#         i = trans(R + L, IP2_TABLE)
#         result += i
#     return result


# def decrypt(origin_str, k):
#     keys = generate_keys(k)
#     str_list = divide(origin_str)
#     result = ""
#     for i in str_list:
#         i = trans(i, IP_TABLE)
#         L, R = i[0:32], i[32:]
#         for j in range(16):
#             L, R = R, xor(L, F(R, keys[15 - j]))
#         i = trans(R + L, IP2_TABLE)
#         result += i
#     result = result.rstrip("0")
#     plaintext = bin2str(result)
#     if plaintext.startswith(VALIDATION_STRING):
#         return plaintext[len(VALIDATION_STRING):]
#     else:
#         return
