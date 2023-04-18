import struct

# def pf(arr):
#     temp = bytearray(len(arr) * 11)
#     temp[:len(arr)] = arr
#     print(temp)
# pf(bytearray("xd".encode("utf-8")))


# Bonus: zapisz 3 liczby: 420, 2137 oraz 1337 w jednym 6 bajtowym buforze, a potem odczytaj wybraną
# Tzn. jak powiem Ci żebyś odczytała mi liczbę nr 2 z bytearray to wyciągniesz tylko ją z bytearray
# jak odczytać tylko część bufora (jak slice)


# 0 - 65535 (2^16 - 1 UwU)



# Napierdol ino funkcyę, która przyjmuje arraja z 16-bitowymi liczbami i zwróć
# bytearraja zawierającego te liczby
def numberArrayToByteArray(arr):
    byteArray = bytearray(len(arr) * 2)
    for i in range(len(arr)):
        byteArray[i*2 : i*2 + 2] = struct.pack("<H", arr[i])
        # 3, 123...
        # 2,4,6
    return byteArray

arra = [2137, 420, 1337]
# print(numberArrayToByteArray(arra))

# Następnie napierdol drugom funkcyję, która weźmie tego bytearraya i zamieni 
# na powrót na tablicę 16 bitowych liczb
def byteArrayToNumberArray(arr):
    temp = []
    for i in range(0, len(arr), 2):
        temp.append(struct.unpack("<H",arr[i:i+2])[0])
    return temp

# print(byteArrayToNumberArray(numberArrayToByteArray(arra)))


# Bonus: napisz funkcję, która przyjmie bytearraya oraz n i zwróci n-liczbę 16 bitową z tego bytearraya
# UwU
def numberFromByteArray(arr, idx):
    return struct.unpack("<H", arr[idx*2: idx*2 + 2])[0]

print(numberFromByteArray(numberArrayToByteArray(arra), 2))





# --Zapisz liczbę 2137 w dwubajtowym buforze, a następnie odczytaj tę liczbę z tego bufora
# array = bytearray(6)
# buffer = struct.pack("<H", 2137)
# array[:len(buffer)] = buffer
# buffer2 = struct.pack("<H", 420)
# print()
# array[2:len(buffer2)] = buffer2

# readed_buffer = struct.unpack("<H", buffer)[0]
# print(struct.unpack("<H", array[2:4])[0])