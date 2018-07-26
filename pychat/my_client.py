from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from packet import Packet

ADDR = ('localhost', 8000)
SERVER_USER = ("server", ADDR)
BUFSIZ = 1024
client_socket = socket(AF_INET, SOCK_STREAM)
username = "none"
USER = (username, "0.0.0.0")

CODE_ERROR_LOGIN = 0
CODE_PLAIN_MSG = 1
CODE_ATTACHMENT_MSG = 2
CODE_LOGOUT = 3
CODE_LOGIN_REQUEST = 4
CODE_LOGIN_SUCCESS  = 5

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            packet = recv(client_socket)
            code = packet.msg_code

            if code == CODE_LOGIN_REQUEST:
                global username
                print packet.text
                username = raw_input('> ')
                send(CODE_LOGIN_REQUEST, SERVER_USER, username)

            elif code == CODE_LOGIN_SUCCESS:
                global USER
                USER = (username, client_socket.getsockname())
                msg = raw_input('> ')
                rec = raw_input("to: ")
                send(CODE_PLAIN_MSG, (rec, "bloop"), msg)

            elif code == CODE_PLAIN_MSG:
                read_msg(packet)
                msg = raw_input('> ')
                rec = raw_input("to: ")
                send(CODE_PLAIN_MSG, (rec, "bloop"), msg)

            elif code == CODE_ATTACHMENT_MSG:
                read_msg(packet, attachment=True)
                msg = raw_input('> ')
                rec = raw_input("to: ")
                send(CODE_PLAIN_MSG, (rec, "bloop"), msg)

            elif code == CODE_LOGOUT:
                print packet.text
                client_socket.close()
                break
        except OSError:  # Possibly client has left the chat.
            break

def read_msg(packet, attachment=False):
    sender = packet.sender[0]
    msg = packet.text
    print "{0} : {1}".format(sender, msg)

    if attachment:
        print "*pic*"

def send(msg_code, rec, msg, attachment="none"):
    packet = Packet(msg_code, USER, rec, msg, attachment)
    client_socket.send(packet.serialize())

def recv(client):
    serial = client.recv(BUFSIZ).decode("utf8")
    packet = Packet.deserialize(serial)
    return packet

if __name__=="__main__":
    # ----Now comes the sockets part----
    #HOST = input('Enter host: ')
    #PORT = input('Enter port: ')
    #if not PORT:
    #    PORT = 8000
    #else:
    #    PORT = int(PORT)

    #ADDR = (HOST, PORT)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()

