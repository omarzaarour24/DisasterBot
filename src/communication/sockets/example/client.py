import socket
import threading
import time
import random
def send_data(client_socket):
    while True:
        try:
            # Rotate from 0 to 180
            for angle in range(0, 181):
                current_distance = random.randint(0, 50)
                angle = 180 - angle
                packet = str("{:05.2f}".format(current_distance)) + str("{:03d}".format(angle))
                client_socket.send(packet.encode())
                time.sleep(0.01)

            # Rotate from 180 to 0
            for angle in range(180, -1, -1):
                current_distance = random.randint(0, 50)
                angle = 180 - angle
                packet = str("{:05.2f}".format(current_distance)) + str("{:03d}".format(angle))
                client_socket.send(packet.encode())
                time.sleep(0.01)
        except:
            print("Error sending data. Closing connection.")
            break

def receive_data(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                print("\nReceived:", data.decode())
        except:
            print("Error receiving data. Closing connection.")
            break

def start_client():
    server_address = ('localhost', 8000)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    print("Connected to the server.")

    send_thread = threading.Thread(target=send_data, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    client_socket.close()

start_client()
