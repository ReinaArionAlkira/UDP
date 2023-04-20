def byte_array_to_bit_array(arr):
    bitArray = []
    for byte in arr:
        for i in range(7,-1, -1):
            bitArray.append(byte>>i&1)
    return(bitArray)

def bit_array_to_byte_array(bits):
    byteArray = []
    byte = 0
    for i in range(len(bits)):
        byte |= bits[i] << 7 - i % 8
        if (i + 1) % 8 == 0:
            byteArray.append(byte)
            byte = 0
    return bytearray(byteArray)

testcase = bytearray([128, 0, 128, 0, 128, 0, 128, 0, 128, 0, 128, 0, 128, 0, 128, 0])

# 1000 0000
# 0000 0000
# 1000 0000
# 0000 0000
# 1000 0000
# 0000 0000
# 1000 0000
# 0000 0000
# 1000 0000
# 0000 0000
# 1000 0000
# 0000 0000
# 1000 0000
# 0000 0000
# 1000 0000
# 0000 0000

# 1111 1111

def interlate128BitBlock(arr: bytearray) -> bytearray:
    temp = byte_array_to_bit_array(arr)
    result = [0] * len(temp)
    for x in range(8):
        for y in range(16):
            result[y * 8 + x] = temp[x * 16 + y]
    return bit_array_to_byte_array(result)

def outerlate128BitBlock(arr: bytearray) -> bytearray:
    temp = byte_array_to_bit_array(arr)
    result = [0] * len(temp)
    for x in range(16):
        for y in range(8):
            result[y * 16 + x] = temp[x * 8 + y]
    return bit_array_to_byte_array(result)
