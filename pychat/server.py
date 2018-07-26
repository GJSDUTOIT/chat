# from socket import AF_INET, socket, SOCK_STREAM
# from threading import Thread
#
# clients = {}
# addresses = {}
#
# HOST = 'localhost'
# PORT = 8000
# BUFSIZ = 1024
# ADDR = (HOST, PORT)
# SERVER = socket(AF_INET, SOCK_STREAM)
# SERVER.bind(ADDR)
#
# def accept_incoming_connections():
#     """Sets up handling for incoming clients."""
#     while True:
#         client, client_address = SERVER.accept()
#         print("%s:%s has connected." % client_address)
#         client.send(bytes("Greetings from the cave!"+
#                           "Now type your name and press enter!").encode("utf8"))
#         addresses[client] = client_address
#         Thread(target=handle_client, args=(client,)).start()
#
# def handle_client(client):  # Takes client socket as argument.
#     """Handles a single client connection."""
#     name = client.recv(BUFSIZ).decode("utf8")
#     welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
#     client.send(bytes(welcome).encode("utf8"))
#     msg = "%s has joined the chat!" % name
#     broadcast(bytes(msg).encode("utf8"))
#     clients[client] = name
#     while True:
#         msg = client.recv(BUFSIZ)
#         if msg != bytes("{quit}").encode("utf8"):
#             broadcast(msg, name+": ")
#         else:
#             client.send(bytes("{quit}").encode("utf8"))
#             client.close()
#             del clients[client]
#             broadcast(bytes("%s has left the chat." % name).encode("utf8"))
#             break
#
# def broadcast(msg, prefix=""):  # prefix is for name identification.
#     """Broadcasts a message to all the clients."""
#     for sock in clients:
#         sock.send(bytes(prefix).encode("utf8")+msg)
#
# if __name__ == "__main__":
#     SERVER.listen(5)  # Listens for 5 connections at max.
#     print("Waiting for connection...")
#     ACCEPT_THREAD = Thread(target=accept_incoming_connections)
#     ACCEPT_THREAD.start()  # Starts the infinite loop.
#     ACCEPT_THREAD.join()
#     SERVER.close()


import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define host
host = 'localhost'

# define the communication port
port = 8000

# Bind the socket to the port
sock.bind((host, port))
# Listen for incoming connections
sock.listen(1)

# Wait for a connection
print 'waiting for a connection'
connection, client = sock.accept()

print connection.getpeername()
print connection.getsockname()

# Receive the data in small chunks and retransmit it

data = connection.recv(16)
print 'received "%s"' % data
if data:

    connection.sendall(data)
else:
    print 'no data from', client

# Close the connection
connection.close()
