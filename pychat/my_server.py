from socket import AF_INET, socket, SOCK_STREAM
from packet import Packet
from threading import Thread

clients = {}
addresses = {}

HOST = 'localhost'
PORT = 8000
BUFSIZ = 1024
ADDRESS = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

# constants
SERVER_USER = ("server", ADDRESS)
CLIENT_USER = ("client", "0.0.0.0")
CODE_ERROR_LOGIN = 0
CODE_PLAIN_MSG = 1
CODE_ATTACHMENT_MSG = 2
CODE_LOGOUT = 3
CODE_LOGIN_REQUEST = 4
CODE_LOGIN_SUCCESS = 5

def accept_connections():
    while True:
        # accept client
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)

        # welcome message
        send(CODE_LOGIN_REQUEST, client, "Hi there! Please enter a username and press enter:")

        # start thread
        ct = Thread(target=handle_client, args=(client,))
        ct.start()

def handle_client(client):
    global CLIENT_USER
    username = recv(client).text

    if (username in clients):
        send(CODE_LOGIN_REQUEST, client, "That username is already taken! Please select another.")
        handle_client(client)

    # welcome client
    clients[username] = client
    CLIENT_USER = (username, client.getsockname())
    send(CODE_LOGIN_SUCCESS, client, "Welcome, {0}!".format(username))

    # display joining status
    broadcast("{0} has joined the chat!".format(username))

    while True:
        packet = recv(client)
        code = packet.msg_code

        if code == CODE_PLAIN_MSG:
            msg = packet.text
            rec = packet.recipient[0] # 1st item in couplet
            sender = packet.sender
            send(code, clients[rec], msg, sender=sender)

        elif code == CODE_ATTACHMENT_MSG:
            msg = packet.text
            rec = packet.recipient[0]  # 1st item in couplet
            sender = packet.sender
            send(code, clients[rec], msg, attachment=packet.attachment, sender=sender)

        elif code == CODE_LOGOUT:
            broadcast("{0} has left the chat.".format(username))
            send(CODE_LOGOUT, client, "Successfully logged out.")
            client.close()
            del clients[client]
            break


def send(msg_code, client, msg, attachment="none", sender=SERVER_USER):
    packet = Packet(msg_code, sender, CLIENT_USER, msg, attachment)
    client.send(packet.serialize())

def recv(client):
    serial = client.recv(BUFSIZ).decode("utf8")
    packet = Packet.deserialize(serial)
    return packet

def broadcast(msg):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients.itervalues():
        send(CODE_PLAIN_MSG, sock, msg)

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections())
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()