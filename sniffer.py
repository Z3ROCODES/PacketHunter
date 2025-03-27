import socket
import struct
import textwrap

def sniff_packets():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    
    while True:
        raw_data, addr = conn.recvfrom(65535)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        print(f"\nEthernet Frame:")
        print(f"Destination: {dest_mac}, Source: {src_mac}, Protocol: {eth_proto}")
        
        if eth_proto == 8:  # IPv4
            (version, header_length, ttl, proto, src, target, data) = ipv4_packet(data)
            print(f"IPv4 Packet: Version: {version}, Header Length: {header_length}, TTL: {ttl}")
            print(f"Protocol: {proto}, Source: {src}, Target: {target}")

def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]

def get_mac_addr(bytes_addr):
    return ':'.join(map('{:02x}'.format, bytes_addr)).upper()

def ipv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]

def ipv4(addr):
    return '.'.join(map(str, addr))

if __name__ == "__main__":
    sniff_packets()
