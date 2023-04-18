# # x = 0b11011101

def byteArrayToBitArray(arr):
    bitArray = []
    for byte in arr:
        for i in range(7,-1, -1):
            bitArray.append(byte>>i&1)
    return(bitArray)

array = [0b10001011, 0b10001111, 0b00001111]
# bitArray = byteArrayToBitArray(bytearray(array))
# byteArray = []
# byte = 0b00000000
# i = 0
# while i < 8:
#     for bit in bitArray:
#         print (f"this is {bit}")
#         byte |= bit<<i
#         i += 1
#         print(byte)
#     i = 0
#     byteArray.append(byte)
# print(byteArray)

# bits = [ 1, 1, 0, 0, 1, 0, 0, 0 ]
# byte = 0b00000000

# for x in range(8):
#     byte |= bits[x] << 7 - x
#     print(bin(byte))
# print(byte)

def bitArrayToByteArray(bits):
    byteArray = []
    byte = 0
    for i in range(len(bits)):
        byte |= bits[i] << 7 - i % 8
        if (i + 1) % 8 == 0:
            byteArray.append(byte)
            byte = 0
    return bytearray(byteArray)

print(bitArrayToByteArray(byteArrayToBitArray("Mmm sekkusu daisku desu".encode("utf-8"))).decode("utf-8"))

# for i in range(7,-1,-1):
#     for bit in bits:
#             print (f"this is {bit}")
#             byte |= bit<<i
#             print(byte)
#     print(byte)