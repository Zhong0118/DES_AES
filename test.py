def hex_to_bin(hex_string):
    # 将16进制字符串转换为整数
    decimal_value = int(hex_string, 16)
    # 将整数转换为二进制字符串，并去掉前缀 '0b'
    binary_string = bin(decimal_value)[2:]
    return binary_string


# # 示例用法
# hex_string = "1b"
# hex_string2 = "fa"
# binary_string = hex_to_bin(hex_string)
# binary_string2 = hex_to_bin(hex_string2)
# print(f"16进制: {hex_string} 转换为二进制: {binary_string}")
# print(f"16进制: {hex_string2} 转换为二进制: {binary_string2}")


# def binary_xor(bin_str1, bin_str2):
#     # 将二进制字符串转换为整数
#     num1 = int(bin_str1, 2)
#     num2 = int(bin_str2, 2)

#     # 进行异或运算
#     xor_result = num1 ^ num2

#     # 将结果转换回二进制字符串，并去掉前缀 '0b'
#     return bin(xor_result)[2:]


# binary_xor_result = binary_xor(binary_string, binary_string2)
# print(f"二进制: {binary_string} 和 {binary_string2} 异或结果: {binary_xor_result}")
hex_string = "01"
hex_string2 = "02"
hex_string3 = "04"
hex_string4 = "08"
hex_string5 = "10"
print(hex_to_bin(hex_string))
print(hex_to_bin(hex_string2))
print(hex_to_bin(hex_string3))
print(hex_to_bin(hex_string4))
print(hex_to_bin(hex_string5))

hex_string6 = "80"
print(hex_to_bin(hex_string6))
hex_string7 = "1b"
print(hex_to_bin(hex_string7))
hex_string8 = "36"
print(hex_to_bin(hex_string8))
