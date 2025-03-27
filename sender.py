import socket
import struct
import time

def send_packet(target_ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    
    packet = struct.pack('!4s4s', socket.inet_aton('192.168.1.100'), socket.inet_aton(target_ip))
    
    while True:
        s.sendto(packet, (target_ip, 80))
        print(f"Packet sent to {target_ip}")
        time.sleep(1)  # Adjust the delay as needed

if __name__ == "__main__":
    target = input("Enter target IP: ")
    send_packet(target)
