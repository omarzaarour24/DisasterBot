import pygame
import socket
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', 'gui')))
from radar import RadarGridVisualizer
import sys

# Server configuration
HOST = "localhost"
PORT = 8000
RUNNING = True

def recvline(sock):
    # Read exactly 8 bytes from the socket
    data = b""
    while len(data) < 8:
        packet = sock.recv(8 - len(data))
        if not packet:
            # Connection closed or no more data
            break
        data += packet

    # Convert the bytes to a string
    line = data.decode("utf-8")  # Adjust the encoding if necessary
    return line


def run_socket_server():
    global RUNNING
    display = RadarGridVisualizer()
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server listening on {}:{}".format(HOST, PORT))

    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print("Client connected:", client_address)
    while RUNNING:
        try:
            data = recvline(client_socket)  # Receive data
            tempd = data[:5]
            tempa = data[5:]
            try:
                a = float(tempa)
            except ValueError:
                a = 0
            try:
                d = float(tempd)
            except ValueError:
                d = -1
            # detect if close is pressed to stop the program
            display.draw_line_and_targets(a, d)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clean_up(client_socket, server_socket)
        except KeyboardInterrupt:
            print("Closing connection...")
            clean_up(client_socket, server_socket)

def clean_up(client_socket, server_socket):
    global RUNNING
    RUNNING = False
    client_socket.close()
    server_socket.close()
    pygame.quit()
    sys.exit(0)

# Start the server in a separate thread
run_socket_server()

