from enum import Enum


class PacketType(Enum):
    MSG = 1
    ACK = 2
    INVALID = 100

x = PacketType.MSG
print(x.value)