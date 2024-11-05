import time
import os
from DES_AES_lib import des_encrypt, des_decrypt, aes_encrypt, aes_decrypt
import DES
import AES

def des_encrypt_time(data, key):
    start_time = time.perf_counter()
    result = DES.encrypt(data, key)
    end_time = time.perf_counter()
    time_cost = end_time - start_time
    return result, time_cost

def des_decrypt_time(data, key):
    start_time = time.perf_counter()
    result = DES.decrypt(data, key)
    end_time = time.perf_counter()
    time_cost = end_time - start_time
    return result, time_cost

def des_encrypt_time_lib(data, key):
    start_time = time.perf_counter()
    result = des_encrypt(data, key)
    end_time = time.perf_counter()
    time_cost = end_time - start_time
    return result, time_cost

def des_decrypt_time_lib(data, key):
    start_time = time.perf_counter()
    result = des_decrypt(data, key)
    end_time = time.perf_counter()
    time_cost = end_time - start_time
    return result, time_cost

def aes_encrypt_time(data, key):
    start_time = time.perf_counter()
    result = AES.AES_encrypt(data, key)
    end_time = time.perf_counter()
    time_cost = end_time - start_time
    return result, time_cost

def aes_decrypt_time(data, key):
    start_time = time.perf_counter()
    result = AES.AES_decrypt(data, key)
    end_time = time.perf_counter()
    time_cost = end_time - start_time
    return result, time_cost

def aes_encrypt_time_lib(data, key):
    start_time = time.perf_counter()
    result = aes_encrypt(data, key)
    end_time = time.perf_counter()
    time_cost = end_time - start_time
    return result, time_cost

def aes_decrypt_time_lib(data, key):
    start_time = time.perf_counter()
    result = aes_decrypt(data, key)
    end_time = time.perf_counter()
    time_cost = end_time - start_time
    return result, time_cost

