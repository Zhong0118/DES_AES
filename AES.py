import base64
from aes_table import *
from hashlib import pbkdf2_hmac

# 这是十进制转16进制
def int2hex(list):
    return [f"{b:02x}" for b in list]

def pad(data):
    """PKCS7填充"""
    if isinstance(data, str):
        data = data.encode()
    padding_length = 16 - (len(data) % 16)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad(data):
    """PKCS7去填充"""
    padding_length = data[-1]
    return data[:-padding_length]

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
def generate_keys(key, state=4):
    k_hex = pbkdf2_hmac("sha256", key.encode("utf-8"), b"salt", 10000, dklen=state * 4)
    rounds = state + 6
    # 初始密钥，直接生成了对应16进制的十进制格式，十进制可直接进行异或运算，也可和16进制进行异或运算，此时的十进制就代表了16进制
    k_hex_list = [int(f"{b:02x}", 16) for b in k_hex]
    keys = [k_hex_list[i:i+4] for i in range(0, len(k_hex_list), 4)]
    for i in range(state, 4 * (rounds + 1)):
        temp = keys[i-1]
        if i % state == 0:
            temp = T_function(temp, i // state - 1)
        elif state > 6 and i % state == 4:
            temp = SubWord(temp)
        keys.append([keys[i-state][j] ^ temp[j] for j in range(4)])
    return keys

'''
AES加密相关的代码
'''
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
    for i in range(8):
        # 如果b的最低位是1，说明是1 3 5 7
        if b & 0x01:
            result ^= a
        # 右移一位
        a = xtime(a)
        b >>= 1
    return result

# 字节替代
def SubBytes(state):
    return [[find_s(state[i][j]) for j in range(4)] for i in range(4)]

# 行移位
def ShiftRows(state):
    return [
        state[0],
        state[1][1:] + state[1][:1],
        state[2][2:] + state[2][:2],
        state[3][3:] + state[3][:3]
    ]

# 列混合
def MixColumns(state):
    return 

# 轮密钥加
def AddRoundKey(state, key):
    return
