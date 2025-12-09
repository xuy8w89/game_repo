import microcontroller
import struct

# =========================
# 数据格式：
# 3s  -> 3个ASCII字符
# 3H  -> 3个无符号short (int, 0~65535)
# 总共 3 + 6 = 9 字节
# =========================
FORMAT = "3s3H"
DATA_SIZE = struct.calcsize(FORMAT)

# -------------------------
# ✅ 保存数据到 Flash
# -------------------------
def save_data(chars, a, b, c):
    packed = struct.pack(FORMAT, chars.encode("ascii"), a, b, c)

    for i in range(DATA_SIZE):
        microcontroller.nvm[i] = packed[i]

# -------------------------
# ✅ 从 Flash 读取数据
# -------------------------
def load_data():
    raw = bytes(microcontroller.nvm[:DATA_SIZE])
    chars, a, b, c = struct.unpack(FORMAT, raw)
    return chars.decode("ascii"), a, b, c


# =========================
# ✅ 测试用例（你可以删掉）
# =========================

# 第一次上电时执行一次保存：
#save_data("ASC", 12, 345, 6789)

# 之后每次上电都能读到：
data = load_data()
print("📦 读取到的数据：", data)
