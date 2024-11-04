import base64


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
        


def str2hex(s):
    try:
        base64_bytes = base64.b64encode(s.encode('utf-8'))
        return base64_bytes.hex()
    except Exception as e:
        print(f"转换错误: {e}")
        return None

def hex2str(hex_str):
    try:
        base64_bytes = bytes.fromhex(hex_str)
        return base64.b64decode(base64_bytes).decode('utf-8')
    except Exception as e:
        print(f"转换错误: {e}")
        return hex_str