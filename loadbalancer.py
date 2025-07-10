import threading
import socket
from urllib import request
import requests

# this library is to simulate the randomness of
# how an LB choose to route a request
import random


# this function is to handle the situation o of a downed server
# specifically preventing the LB from routing to a dead server
# and having, dropped request.
def health_check():
    global healthy_servers
    for server in backend_servers:
        try:
            health_response = requests.get(f"http://{server[0]}:{server[1]}/health")
            if health_response.status_code == 200:
                if server not in healthy_servers:
                    healthy_servers.append(server)
            else:
                if server in healthy_servers:
                    healthy_servers.remove(server)
        except Exception as e:
            print(f"Error during health check for server {server}: {e}")
            if server in healthy_servers:
                healthy_servers.remove(server)


def handle_client(client_socket):

    request_data = client_socket.recv(1024).decode()

    if not healthy_servers:
        client_socket.sendall(
            b"HTTP/1.1 503 service is unvailable \r\n\r\nNo Healthy upstream unavailable"
        )
        client_socket.close()

    print("Received request from: ", client_socket.getpeername())
    print(request_data)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend_socket:

        # This is the address of server that the request is being forwarded to
        backend_address = random.choice(backend_servers)
        backend_socket.connect(backend_address)
        backend_socket.sendall(request_data.encode())

        # receive the data
        response_data = backend_socket.recv(1024)
        print(f"The response data is {response_data}")

    client_socket.sendall(response_data)
    client_socket.close()


def start_load_balancer(port):
    # checks the health of servers on start up
    health_check()

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # bind the socket
        server_socket.bind(("localhost", port))

        # Listen for incoming requests
        server_socket.listen()
        print(f"Load Balancer is listening at port {port}....\n")

        while True:
            # Accept a new connection from the client
            client_socket, client_address = server_socket.accept()

            # Handle forwarding the data to destination servers in seperate threads
            threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    # pool of  servers that traffic is being routed to
    backend_servers = [("localhost", 6400), ("localhost", 6500), ("localhost", 6700)]
    healthy_servers = []
    # server that this is being forwarded to must already be running
    start_load_balancer(9000)
