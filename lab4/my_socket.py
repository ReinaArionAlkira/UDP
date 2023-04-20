from enum import Enum
import math
import queue
import socket
import struct
from threading import Thread
from time import sleep
import hamming

PACKET_NUM_SIZE = 2
PACKET_PADDING_SIZE = 1
PACKET_TYPE_SIZE = 1
HEADER_SIZE = PACKET_NUM_SIZE + PACKET_PADDING_SIZE + PACKET_TYPE_SIZE
# before hamming encoded
MSG_PACKET_SIZE = 11 * 8 # 128 byte hamming encoded
MSG_PACKET_PAYLOAD_SIZE = MSG_PACKET_SIZE - HEADER_SIZE
MINIMAL_PACKET_SIZE = 11 # 16 byte hamming encoded
MINIMAL_PAYLOAD_SIZE = 7

class PacketType(Enum):
    MSG = 1
    ACK = 2
    EOF = 3
    INVALID = 100

class ParsedPacket:
    def __init__(self, type: PacketType, valid: bool, payload: bytearray, num: int):
        self.type = type
        self.payload = payload
        self.valid = valid
        self.num = num

class SendItem:
    def __init__(self, packet: bytearray, addr: tuple[str, int], retry_until_acknowledged: bool = False):
        self.packet = packet
        self.addr = addr
        self.retry_until_acknowledged = retry_until_acknowledged

class MySocket:
    def __init__(self):
        self.internal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.received_queue = queue.Queue[tuple[str, tuple[str, int]]]()
        self.send_queue = queue.Queue[SendItem]()
        self.ack_queue = queue.Queue[bool]()
        self.recvthread = Thread(target=self.recvloop)
        self.sendthread = Thread(target=self.sendloop)
        self.current_send_item: SendItem | None = None
        self.last_received_num = -1
        self.invalid_same_packets = []
        self.final_recv_message = bytearray()
    
    def bind(self, addr: tuple[str, int]):
        self.internal_socket.bind(addr)
        self.recvthread.start()
        self.sendthread.start()
    
    def sendto(self, msg: bytearray, addr: tuple[str, int]):
        packets_iter = self.split_message_into_packets(msg)

        for packet in packets_iter:
            self.send_queue.put(SendItem(packet, addr, True))

    def sendack(self, addr: tuple[str, int], num: int):
        packet = self.create_ack_packet(num)
        self.send_queue.put(SendItem(packet, addr))

    def recvfrom(self, buf_size: int):
        return self.received_queue.get()

    def recvloop(self):
        while True:
            bytes, addr = self.internal_socket.recvfrom(1024 * 1024)
            packet: ParsedPacket = self.process_packet(bytes)
            if not packet.valid:
                continue

            # since python 3.10, before use ifs XD
            match packet.type:
                case PacketType.MSG:
                    if (self.last_received_num == packet.num):
                        self.sendack(addr, packet.num)
                        continue
                    # self.received_queue.put((packet.payload, addr))
                    self.final_recv_message += packet.payload
                    self.last_received_num = packet.num
                    self.sendack(addr, packet.num)
                    print(f"Sent ack num: {packet.num}")
                case PacketType.EOF:
                    print("EOF Received")
                    self.received_queue.put((self.final_recv_message, addr))
                    self.final_recv_message = bytearray(0)
                    self.sendack(addr, packet.num)
                case PacketType.ACK:
                    self.ack_queue.put(True)
                

    def sendloop(self):
        sent = 0
        while True:
            if self.current_send_item == None:
                self.current_send_item = self.send_queue.get()

            sent += self.internal_socket.sendto(self.current_send_item.packet, self.current_send_item.addr)
            print(f"Sent: {sent}")

            if not self.current_send_item.retry_until_acknowledged:
                self.current_send_item = None
                continue
            
            try:
                self.ack_queue.get(timeout=0.02)
                self.current_send_item = None
            except:
                pass

    def split_message_into_packets(self, msg: bytearray):
        blocks = math.ceil(len(msg) / MSG_PACKET_PAYLOAD_SIZE)
        for i in range(blocks):
            offset = i * MSG_PACKET_PAYLOAD_SIZE
            end = offset + MSG_PACKET_PAYLOAD_SIZE
            yield self.create_msg_packet(i % 65535, msg[offset:end])
        
        yield self.create_eof_packet(i + 1)

    def create_msg_packet(self, num: int, payload: bytearray) -> bytearray:
        if len(payload) > MSG_PACKET_PAYLOAD_SIZE:
            raise Exception(f"Payload size {payload} is too much for single packet, max is {MSG_PACKET_PAYLOAD_SIZE}")

        padding_size = MSG_PACKET_PAYLOAD_SIZE - len(payload)
        padding_size_buf = struct.pack("B", padding_size)
        padding = bytearray(padding_size)
        type_buf = struct.pack("B", PacketType.MSG.value)
        packet_num = struct.pack("<H", num)
        return self.encode_packet(packet_num + type_buf + padding_size_buf + payload + padding)
    
    def create_type_only_packet(self, num: int, type: PacketType):
        padding_size = MINIMAL_PACKET_SIZE - HEADER_SIZE
        padding_size_buf = struct.pack("B", padding_size)
        padding = bytearray(padding_size)
        type_buf = struct.pack("B", type.value)
        packet_num = struct.pack("<H", num)
        return self.encode_packet(packet_num + type_buf + padding_size_buf + padding)

    def create_ack_packet(self, num: int) -> bytearray:
        # Serwer zakłóca wiadomość, ale nie jej rozmiar!
        # Minimalna długość pakietu to 16 bajtów, gdyż takie przyjęliśmy bloki do kodowania hamminga
        # Ale pakiet potwierdzający nie potrzebuje przenosić żadnych danych, trzeba go tylko rozróżnić
        # Więc jak pakiet będzie miał długość poniżej 16 bajtów to będzie znaczyło, że jest to
        # pakiet potwierdzający. I zakłócenia nie zakłócą nam potwierdzenia!
        return bytearray(2)
    
    def create_eof_packet(self, num: int) -> bytearray:
        return self.create_type_only_packet(num, PacketType.EOF)
    
    def encode_packet(self, raw: bytearray) -> bytearray:
        return hamming.interlate_whole(hamming.hamming_encode(raw))
    
    def process_packet(self, raw: bytearray) -> ParsedPacket:
        # Serwer zakłóca wiadomość, ale nie jej rozmiar!
        # Minimalna długość pakietu to 16 bajtów, gdyż takie przyjęliśmy bloki do kodowania hamminga
        # Ale pakiet potwierdzający nie potrzebuje przenosić żadnych danych, trzeba go tylko rozróżnić
        # Więc jak pakiet będzie miał długość poniżej 16 bajtów to będzie znaczyło, że jest to
        # pakiet potwierdzający. I zakłócenia nie zakłócą nam potwierdzenia!
        if (len(raw) < 16):
            return ParsedPacket(PacketType.ACK, True, bytearray(0), 0)

        decoded, valid = hamming.hamming_decode(hamming.outerlate_whole(raw))

        if not valid:
            self.invalid_same_packets.append(raw)
            if len(self.invalid_same_packets) >= 3:
                decoded, valid = hamming.hamming_decode(
                    hamming.outerlate_whole(
                        self.try_fix_from_invalid_packets()
                    )
                )
                num = struct.unpack("<H", decoded[0:2])[0]

        if valid:
            self.invalid_same_packets = []

        try:
            packet_type = PacketType(decoded[2])
        except:
            packet_type = PacketType.INVALID
        
        num = struct.unpack("<H", decoded[0:2])[0]
        padding_size = decoded[3]
        payload = decoded[4:len(decoded) - padding_size]
        return ParsedPacket(packet_type, valid, payload, num)
    
    def try_fix_from_invalid_packets(self):
        first_packet = self.invalid_same_packets[0]
        ret = bytearray(len(first_packet))

        for i in range(len(first_packet)):
            bytes = []
            for packet in self.invalid_same_packets:
                bytes.append(packet[i])
            ret[i] = self.most_common_byte(bytes)
        return ret

    def most_common_byte(self, bytes: list):
        counts = {}
        for b in bytes:
            if b in counts:
                counts[b] += 1
            else:
                counts[b] = 1

        most_common = None
        max_count = 0
        for b, count in counts.items():
            if count > max_count:
                most_common = b
                max_count = count
        return most_common
        