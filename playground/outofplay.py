def byteArrayToBitArray(arr):
    bitArray = []
    for byte in arr:
        for i in range(7,-1, -1):
            bitArray.append(byte>>i&1)
    return(bitArray)

def bitArrayToByteArray(bits):
    byteArray = []
    byte = 0
    for i in range(len(bits)):
        byte |= bits[i] << 7 - i % 8
        if (i + 1) % 8 == 0:
            byteArray.append(byte)
            byte = 0
    return bytearray(byteArray)

print(bitArrayToByteArray(byteArrayToBitArray("Cep".encode("utf-8"))).decode("utf-8"))