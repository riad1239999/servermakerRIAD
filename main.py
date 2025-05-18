import socket
import threading
import time
import sys

IP_LIST_FILE = "THEipList.txt"
START_PORT = 500
END_PORT = 600   # Adjust as needed
DELAY_SECONDS = 1

def write_ip_port(ip, port):
    with open(IP_LIST_FILE, "a") as f:
        f.write(f"{ip}:{port}\n")

def handle_client(client_socket, addr, port):
    try:
        client_socket.sendall(f"Welcome to servermakerRIAD on port {port}\n".encode())
    except Exception as e:
        print(f"Error sending to client {addr}: {e}")
    finally:
        client_socket.close()

def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(('0.0.0.0', port))
            return True
        except OSError:
            return False

def server_thread(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('0.0.0.0', port))
    except OSError:
        print(f"Port {port} could not be bound, skipping.")
        return False

    server.listen(5)
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    write_ip_port(local_ip, port)
    print(f"ip created {local_ip}:{port}")

    try:
        while True:
            client, addr = server.accept()
            threading.Thread(target=handle_client, args=(client, addr, port), daemon=True).start()
    except Exception as e:
        print(f"Server on port {port} error: {e}")
    finally:
        server.close()
    return True

def create_servers_no_skip(start_port=START_PORT, end_port=END_PORT, delay=DELAY_SECONDS):
    print(f"Starting servermakerRIAD on ports {start_port} to {end_port}")
    port = start_port
    while port <= end_port:
        if is_port_free(port):
            threading.Thread(target=server_thread, args=(port,), daemon=True).start()
            time.sleep(delay)
            # After delay, if port still free, try again (or increment)
            if is_port_free(port):
                print(f"Port {port} did not open properly, retrying...")
            else:
                port += 1
        else:
            print(f"Port {port} in use or blocked, skipping.")
            port += 1

if __name__ == "__main__":
    try:
        create_servers_no_skip()
    except KeyboardInterrupt:
        print("\nShutting down servermakerRIAD.")
        sys.exit(0)
