# napisz funkcję która przyjmie bytearray
# i podzieli na tablicę 128 bajtowych bytearray

import math


test = ("AAAAAAAA" * 124).encode()

def split_bytearray(arr: bytearray, length: int) -> list:
    splited = []
    _128_bit_block = math.ceil(len(arr) / length)
    for i in range(_128_bit_block):
        block = bytearray(length)
        temp = bytearray(arr[i*length : i*length + length])
        block[:len(temp)] = temp
        splited.append(block)
        print(len(block))

    return splited

print(split_bytearray(test, 32))