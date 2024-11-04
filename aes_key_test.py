import base64
from aes_table import *
from AES import AES_encrypt, AES_decrypt
from hashlib import pbkdf2_hmac

# 找到s盒中的值
def find_s(num):
    return s_box[num // 16][num % 16]
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
def generate_keys(keys, state=4):
    rounds = state + 6
    keys = [int(b, 16) for b in keys]
    keys = [keys[i:i+4] for i in range(0, len(keys), 4)]
    for i in range(state, 4 * (rounds + 1)):
        temp = keys[i-1]
        if i % state == 0:
            temp = T_function(temp, i // state - 1)
        elif state == 8 and i % state == 4:
            temp = SubWord(temp)
        keys.append([keys[i-state][j] ^ temp[j] for j in range(4)])
    return keys


def generate_keys2(keys, state=4):
    rounds = state + 6
    keys1 = [int(b, 16) for b in keys]
    keys = []
    for i in range(0, state):
        column = []
        for j in range(0, 4):
            column.append(keys1[j * state + i])
        keys.append(column)
    for i in range(state, 4 * (rounds + 1)):
        temp = keys[i-1]
        if i % state == 0:
            temp = T_function(temp, i // state - 1)
        elif state > 6 and i % state == 4:
            temp = SubWord(temp)
        keys.append([keys[i-state][j] ^ temp[j] for j in range(4)])
    return keys


if __name__ == "__main__":
    key = '2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c'
    test_text = 'hello, world! i love you'
    key = key.split(' ')
    
    print("=== AES加密解密测试 ===")
    print("原始文本:", test_text)
    print("密钥:", key)
    
    # 加密
    print("\n=== 加密过程 ===")
    encrypted = AES_encrypt(test_text, key)
    if encrypted:
        print("加密结果(base64):", encrypted.decode())
        
        # 解密
        print("\n=== 解密过程 ===")
        decrypted = AES_decrypt(encrypted, key)
        print("解密结果:", decrypted)
        
        # 验证
        print("\n=== 验证 ===")
        print("原始文本:", test_text)
        print("解密文本:", decrypted)
        print("解密正确:", test_text == decrypted)
    else:
        print("加密失败")



# 3243f6a8885a308d313198a2e0370734

# print("===================")
# key2 = '8e 73 b0 f7 da 0e 64 52 c8 10 f3 2b 80 90 79 e5 62 f8 ea d2 52 2c 6b 7b'
# keys2 = key2.split(' ')
# generate_keys(keys2, 6)
# print("===================")
# key3 = '60 3d eb 10 15 ca 71 be 2b 73 ae f0 85 7d 77 81 1f 35 2c 07 3b 61 08 d7 2d 98 10 a3 09 14 df f4'
# keys3 = key3.split(' ')
# generate_keys(keys3, 8)

