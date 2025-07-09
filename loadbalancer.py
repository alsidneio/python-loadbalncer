import threading
import socket


def handle_client(client_socket):

    request_data = client_socket.recv(1024).decode()

    print("Received request from: ", client_socket.getpeername())
    print(request_data)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend_socket:

        # This is the address of server that the request is being forwarded to
        backend_address = ("localhost", 6400)
        backend_socket.connect(backend_address)
        backend_socket.sendall(request_data.encode())

        # receive the data
        response_data = backend_socket.recv(1024)
        print(f"The response data is {response_data}")

    client_socket.sendall(response_data)
    client_socket.close()


def start_load_balancer(port):
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
    # server that this is being forwarded to must already be running 
    start_load_balancer(9000)
