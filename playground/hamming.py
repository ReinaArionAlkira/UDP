import math
import struct


hamming15_11BitPositions = [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]

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

# bytearray required
def hamming_encode(buf: bytearray):
    # 8 * 16 hamming bits ({16,11})
    # each block of {16,11} hamming code encodes 11 bits of the message
    # this is not much ideal because each byte has 8 bits
    # so to make it easier we round it to lowest common multiple
    _128_bit_blocks = math.ceil(len(buf) / 11)
    temp = bytearray(_128_bit_blocks * 11)
    temp[:len(buf)] = buf
    # Empty storage for hamming encoded message in this bytearray
    encoded = bytearray(16 * _128_bit_blocks)

    word = 0
    i = 0
    for bit in byte_array_to_bit_array(temp):
        word |= bit << hamming15_11BitPositions[i % 11]
        i += 1
        if i % 11 == 0 :
            offset = int(i / 11 * 2 - 2)
            encoded[offset : offset + 2] = struct.pack("<H", word)
            word = 0

    return encoded
    
def hamming_decode(buf: bytearray):
    if len(buf) % 16 != 0:
        raise Exception("Invalid buffer, it must contain blocks of 16 bytes length")
    _128_bit_blocks = math.ceil(len(buf) / 16)
    decoded = bytearray(11 * _128_bit_blocks)
    for i in range(_128_bit_blocks):
        bits = []
        block = buf[i*16 : i*16 + 16]

        for j in range(8):
            word = struct.unpack("<H", block[j*2:j*2+2])[0]

        # message fragment for bits
            for k in range(11):
                bits.append((word >> hamming15_11BitPositions[k]) & 1)
        
        b = bit_array_to_byte_array(bits)
        decoded[i*11: i*11 + 11] = b

    return decoded


ham = hamming_encode("elo320".encode())
print(hamming_decode(ham).decode())
    
