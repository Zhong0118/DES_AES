from time_compare import *

def generate_test_data(size):
    """生成指定大小的测试数据"""
    return ''.join(chr(i % 256) for i in range(size))

def run_comparison():
    key = "this is a secret key"
    data_sizes = [1024, 10240, 102400]
    results = {
        'custom_des_enc': [],
        'lib_des_enc': [],
        'custom_aes_enc': [],
        'lib_aes_enc': [],
        'custom_des_dec': [],
        'lib_des_dec': [],
        'custom_aes_dec': [],
        'lib_aes_dec': []
    }
    
    for size in data_sizes:
        print(f"\nThe size of data: {size} bytes")
        test_data = generate_test_data(size)
        
        # 加密测试
        custom_des_enc, time1 = des_encrypt_time(test_data, key)
        lib_des_enc, time2 = des_encrypt_time_lib(test_data, key)
        custom_aes_enc, time3 = aes_encrypt_time(test_data, key)
        lib_aes_enc, time4 = aes_encrypt_time_lib(test_data, key)
        
        # 解密测试
        _, time5 = des_decrypt_time(custom_des_enc, key)
        _, time6 = des_decrypt_time_lib(lib_des_enc, key)
        _, time7 = aes_decrypt_time(custom_aes_enc, key)
        _, time8 = aes_decrypt_time_lib(lib_aes_enc, key)
        
        # 存储结果
        results['custom_des_enc'].append(time1)
        results['lib_des_enc'].append(time2)
        results['custom_aes_enc'].append(time3)
        results['lib_aes_enc'].append(time4)
        results['custom_des_dec'].append(time5)
        results['lib_des_dec'].append(time6)
        results['custom_aes_dec'].append(time7)
        results['lib_aes_dec'].append(time8)
        
        # 打印当前大小的结果
        print(f"\nEncryption time:")
        print(f"Custom DES: {time1:.6f} 秒")
        print(f"Library DES: {time2:.6f} 秒")
        print(f"Custom AES: {time3:.6f} 秒")
        print(f"Library AES: {time4:.6f} 秒")
        
        print(f"\nDecryption time:")
        print(f"Custom DES: {time5:.6f} 秒")
        print(f"Library DES: {time6:.6f} 秒")
        print(f"Custom AES: {time7:.6f} 秒")
        print(f"Library AES: {time8:.6f} 秒")
    
    return results, data_sizes

def print_summary(results, data_sizes):
    print("\n=== Summary ===")
    print("Data size(bytes) | Custom DES | Library DES | Custom AES | Library AES")
    print("-" * 70)
    
    print("Encryption time(seconds):")
    for size, times in zip(data_sizes, zip(
        results['custom_des_enc'],
        results['lib_des_enc'],
        results['custom_aes_enc'],
        results['lib_aes_enc']
    )):
        print(f"{size:13} | {times[0]:.6f} | {times[1]:.6f} | {times[2]:.6f} | {times[3]:.6f}")
    
    print("\nDecryption time(seconds):")
    for size, times in zip(data_sizes, zip(
        results['custom_des_dec'],
        results['lib_des_dec'],
        results['custom_aes_dec'],
        results['lib_aes_dec']
    )):
        print(f"{size:13} | {times[0]:.6f} | {times[1]:.6f} | {times[2]:.6f} | {times[3]:.6f}")

if __name__ == "__main__":
    results, data_sizes = run_comparison()
    print_summary(results, data_sizes)
