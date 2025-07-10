import socket
import threading

# TODO: create a repsonse object so you can paramaterize the printed response


def start_backend_server(port):
    # create a TCP/IP to communicate on
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # bind the socket
        server_socket.bind(("localhost", port))

        # Listen for incoming requests
        server_socket.listen()
        print(f"Backend server is running at port {port}....\n")

        while True:
            # Accept a new connection from the client
            client_socket, client_address = server_socket.accept()

            # Receiuve the request fromt the client
            request_data = client_socket.recv(1024).decode()

            # log the request data
            print("Received request from : ", client_socket.getpeername())
            print(request_data)

            response = f"HTTP/1.1 200 OK\r\n\r\nHello FROM THE SERVERSIDE!...communicating on port: {port}"
            client_socket.sendall(response.encode())

            # close the client socket
            client_socket.close()


if __name__ == "__main__":
    ports = [6400, 6500]
    for port in ports:
        thread = threading.Thread(target=start_backend_server, args=(port,))
        thread.start()
