import base64
from aes_table import *
from hashlib import pbkdf2_hmac

"""
注意：本实现采用横向（row-major）方式处理状态矩阵，
与AES标准的纵向（column-major）实现有所不同。
同时过程中的数据的运算大部分由16进制转换为十进制，十进制进行运算，感官上有一定的混乱，但是实际上是正确的
因为转成数字的话可直接进行运算，有的步骤貌似会把十六进制看作字符串，此时的异或操作会失败
矩阵表示方式为：
[
    [0,  1,  2,  3 ],
    [4,  5,  6,  7 ],
    [8,  9,  10, 11],
    [12, 13, 14, 15]
]
而不是标准的：
[
    [0,  4,  8,  12],
    [1,  5,  9,  13],
    [2,  6,  10, 14],
    [3,  7,  11, 15]
]
"""

# 这是十进制转16进制
def int2hex(list):
    return [f"{b:02x}" for b in list]

def str2hex(s):
    return s.encode('utf-8').hex()

def hex2str(hex_str):
    try:
        return bytes.fromhex(hex_str).decode('utf-8')
    except UnicodeDecodeError:
        try:
            return bytes.fromhex(hex_str).decode('latin1')
        except:
            return hex_str  # 如果都失败，返回原始十六进制

def pad(data):
    hex_str = str2hex(data)
    if hex_str is None:
        return None
    try:
        bytes_data = bytes.fromhex(hex_str)
        padding_length = 16 - (len(bytes_data) % 16)
        padded_data = bytes_data + bytes([padding_length] * padding_length)
        return padded_data.hex()
    except Exception as e:
        print(f"填充错误: {e}")
        return None

def unpad(data):
    if not data:
        return ''
    try:
        bytes_data = bytes.fromhex(data)
        padding_length = bytes_data[-1]
        if padding_length > 16:
            return data
        if not all(x == padding_length for x in bytes_data[-padding_length:]):
            return data
        unpadded_data = bytes_data[:-padding_length]
        return unpadded_data.hex()
    except Exception as e:
        print(f"去填充错误: {e}")
        return data

# 找到s盒中的值
def find_s(num):
    return s_box[num // 16][num % 16]

'''
密钥生成相关的代码
'''
# 字节替代
def SubWord(list):
    return [find_s(list[j]) for j in range(4)]
# 轮转
def RotWord(list):
    return list[1:] + list[:1]
# T函数
def T_function(list, i):
    list = RotWord(list)
    list = SubWord(list)
    list[0] = list[0] ^ Rcon[i]
    return list

# state只分为4,6,8三种
def generate_keys(key, condition=4):
    k_hex = pbkdf2_hmac("sha256", key.encode("utf-8"), b"salt", 10000, dklen=condition * 4)
    rounds = condition + 6
    # 初始密钥，直接生成了对应16进制的十进制格式，十进制可直接进行异或运算，也可和16进制进行异或运算，此时的十进制就代表了16进制
    k_hex_list = [int(f"{b:02x}", 16) for b in k_hex]
    keys = [k_hex_list[i:i+4] for i in range(0, len(k_hex_list), 4)]
    for i in range(condition, 4 * (rounds + 1)):
        temp = keys[i-1]
        if i % condition == 0:
            temp = T_function(temp, i // condition - 1)
        elif condition > 6 and i % condition == 4:
            temp = SubWord(temp)
        keys.append([keys[i-condition][j] ^ temp[j] for j in range(4)])
    return keys


'''
AES加密相关的代码
'''
# 字节和矩阵相互转换
def bytes2matrix(hex_list):
    # 将16进制字符串转换为矩阵
    hex_list = [int(hex_list[i:i+2], 16) for i in range(0, len(hex_list), 2)]
    return [hex_list[i:i+4] for i in range(0, len(hex_list), 4)]
def matrix2bytes(matrix):
    # 将矩阵中的每个元素转换为16进制字符串
    result = ''
    for i in range(4):
        for j in range(4):
            result += f"{matrix[i][j]:02x}"
    return result



# 乘法GF(2^8)
# 这一部分就是右移操作，基于2倍
def xtime(num):
    # 左移一位
    shift_num = num << 1
    # 如果最高位是1，则需要异或0x1b
    # 1000 0000
    if num & 0x80:
        # 0001 1011
        shift_num = shift_num ^ 0x1b
    return shift_num

'''
真要相乘的时候需要借助xtime函数，因为是基于2倍异或，实际上result是我们需要的结果，无论是乘1 2 3 4 5... 我们可以认为涉及到2的时候会进行xtime
然后1就是本身，2是xtime一次，3是本身的结果和xtime之后的结果进行异或，4是xtime两次之后的结果
只考虑result的话，实际上只有当b的1都过去了，后续a咋变都不影响，但是每当b达到了1，说明result需要和a本身进行异或操作，但是a的值是一直变的，因为涉及到1
就说明多了一次异或，a本身是跟着b需要一直乘2的
'''
def mul_GF(a, b):
    result = 0
    for _ in range(8):
        # 如果b的最低位是1，说明是1 3 5 7
        if b & 0x01:
            result ^= a
        # 右移一位
        a = xtime(a)
        b >>= 1
    return result & 0xFF

# 字节替代
def SubBytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = find_s(state[i][j])
    return state


'''# 之前的按照列的方式
[[0, 4, 10, 12],
 [1, 5, 11, 13],
 [2, 6, 14, 15],
 [3, 7, 12, 14]]
# 移动后
[[0, 4, 10, 12],
 [5, 11, 13, 1],
 [14, 15, 2, 6],
 [14, 3, 7, 12]]

# 现在的按照行的方式
[[0, 1, 2, 3],
 [4, 5, 6, 7],
 [8, 9, 10, 11],
 [12, 13, 14, 15]]
# 移动后
[[0, 5, 10, 15],
 [4, 9, 14, 3],
 [8, 13, 2, 7],
 [12, 1, 6, 11]]'''
# 行移位
def ShiftRows(state):
    return [
        [state[0][0], state[1][1], state[2][2], state[3][3]],  # 对角线1
        [state[1][0], state[2][1], state[3][2], state[0][3]],  # 对角线偏移1
        [state[2][0], state[3][1], state[0][2], state[1][3]],  # 对角线偏移2
        [state[3][0], state[0][1], state[1][2], state[2][3]]   # 对角线偏移3
    ]

# 列混合
def MixColumns(state):
    """行混合（基于原列混合修改）
    直接处理每一行，保持相同的乘法系数顺序
    """
    for i in range(4):
        row = [state[i][j] for j in range(4)]
        state[i][0] = mul_GF(0x02, row[0]) ^ mul_GF(0x03, row[1]) ^ mul_GF(0x01, row[2]) ^ mul_GF(0x01, row[3])
        state[i][1] = mul_GF(0x01, row[0]) ^ mul_GF(0x02, row[1]) ^ mul_GF(0x03, row[2]) ^ mul_GF(0x01, row[3])
        state[i][2] = mul_GF(0x01, row[0]) ^ mul_GF(0x01, row[1]) ^ mul_GF(0x02, row[2]) ^ mul_GF(0x03, row[3])
        state[i][3] = mul_GF(0x03, row[0]) ^ mul_GF(0x01, row[1]) ^ mul_GF(0x01, row[2]) ^ mul_GF(0x02, row[3])
    return state

# 轮密钥加
def AddRoundKey(state, keys, round):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= keys[round * 4 + i][j]
    return state

def AES_encrypt(plaintext, key, condition=4):
    keys = generate_keys(key, condition)
    padded_plaintext = pad(plaintext)
    ciphertext = ''
    for i in range(len(padded_plaintext) // 32):
        block = padded_plaintext[i * 32:(i + 1) * 32]
        state = bytes2matrix(block)
        state = AddRoundKey(state, keys, 0)
        for i in range(1, condition + 7):
            state = SubBytes(state)
            state = ShiftRows(state)
            if i != condition + 6:
                state = MixColumns(state)
            state = AddRoundKey(state, keys, i)
        ciphertext += matrix2bytes(state)
    return ciphertext



def inv_find_s(num):
    return inv_s_box[num // 16][num % 16]

def inv_SubBytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = inv_find_s(state[i][j])
    return state

def inv_ShiftRows(state):
    return [
        [state[0][0], state[3][1], state[2][2], state[1][3]],
        [state[1][0], state[0][1], state[3][2], state[2][3]],
        [state[2][0], state[1][1], state[0][2], state[3][3]],
        [state[3][0], state[2][1], state[1][2], state[0][3]]
    ]

def inv_MixColumns(state):
    for i in range(4):
        row = [state[i][j] for j in range(4)]
        state[i][0] = mul_GF(0x0e, row[0]) ^ mul_GF(0x0b, row[1]) ^ mul_GF(0x0d, row[2]) ^ mul_GF(0x09, row[3])
        state[i][1] = mul_GF(0x09, row[0]) ^ mul_GF(0x0e, row[1]) ^ mul_GF(0x0b, row[2]) ^ mul_GF(0x0d, row[3])
        state[i][2] = mul_GF(0x0d, row[0]) ^ mul_GF(0x09, row[1]) ^ mul_GF(0x0e, row[2]) ^ mul_GF(0x0b, row[3])
        state[i][3] = mul_GF(0x0b, row[0]) ^ mul_GF(0x0d, row[1]) ^ mul_GF(0x09, row[2]) ^ mul_GF(0x0e, row[3])
    return state


def AES_decrypt(ciphertext, key, condition=4):
    keys = generate_keys(key, condition)
    padded_ciphertext = ciphertext
    plaintext = ''
    for i in range(len(padded_ciphertext) // 32):
        block = padded_ciphertext[i * 32:(i + 1) * 32]
        state = bytes2matrix(block)
        state = AddRoundKey(state, keys, condition + 6)
        for i in range(condition + 5, -1, -1):
            state = inv_ShiftRows(state)
            state = inv_SubBytes(state)
            state = AddRoundKey(state, keys, i)
            if i != 0:
                state = inv_MixColumns(state)
        plaintext += matrix2bytes(state)
    plaintext = unpad(plaintext)
    return hex2str(plaintext)



