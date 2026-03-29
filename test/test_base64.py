# Python: 粗略判断并尝试Base64解码
import base64
import re

s = "20UnPKRWdL53l3i/dcR/v3uXGj0lBqK80HIpPeJqeD/JuHO+gqecQ4ankMF7BCtC"

# Base64字符集检测
is_b64_charset = re.fullmatch(r"[A-Za-z0-9+/=]+", s) is not None

print("Base64字符集:", is_b64_charset)
print("长度:", len(s), "是否4的倍数:", len(s) % 4 == 0)

# 尝试解码（自动补齐=）
padding = "=" * (-len(s) % 4)
try:
    data = base64.b64decode(s + padding, validate=False)
    print("解码字节长度:", len(data))
    print("前16字节hex:", data[:16].hex())
    # 尝试作为UTF-8文本
    try:
        print("UTF-8文本:", data.decode("utf-8"))
    except UnicodeDecodeError:
        print("UTF-8文本: 无法解码（可能是二进制数据）")
except Exception as e:
    print("解码失败:", e)