import Tkinter as tk
from Tkinter import *
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
CODE_USER_LOGIN = 6
CODE_USER_LOGOUT = 7

active_users = {}

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

            elif code == CODE_PLAIN_MSG:
                read_msg(packet)

            elif code == CODE_ATTACHMENT_MSG:
                read_msg(packet, attachment=True)

            elif code == CODE_USER_LOGIN:
		active_users = parse_users(packet.text)
		repop_users()

            elif code == CODE_USER_LOGOUT:
                active_users = parse_users(packet.text)
		repop_users()

            elif code == CODE_LOGOUT:
                print packet.text
                client_socket.close()
                break
        except OSError:  # Possibly client has left the chat.
            break

def read_msg(packet, attachment=False):
    sender = packet.sender[0]
    msg = packet.text
    disp = "{0} : {1}".format(sender, msg)
    displayArea.insert(disp)

    if attachment:
        print "*pic*"

def send(msg_code, rec, msg, attachment="none"):
    packet = Packet(msg_code, USER, rec, msg, attachment)
    client_socket.send(packet.serialize())

def recv(client):
    serial = client.recv(BUFSIZ)
    packet = Packet.deserialize(serial)
    return packet

def parse_users(s):
    active_users = {}
    users = s.split("%")
    for user in users:
	uname = user.split("@")[0]
	addr = user.split("@")[1]
	active_users[uname] = addr
        print uname, addr


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


### GUI binding ###

def repop_users():
    listbox.delete(0,'end')
    for user in active_users:
    	listbox.insert(END, user)

def btn_send(event=None):
    msg = inputArea.get()
    rec = listbox.get(listbox.curselection())
    send(CODE_PLAIN_MSG, (rec, active_users[rec]), msg)

def on_closing(event=None):
    # close
    return

### elements ###
top = tk.Tk()
top.title("Chatter")
top.resizable(0,0)
top.geometry("600x400")
# ------------------------------------------------------------------------------
listscroll = Scrollbar(top)
listscroll.place(x=201, y=0, width=20, height=800)

listbox = Listbox(top)
listbox.place(x=0, y=0, width=200, height=800)
#contacts = ["Chat Room", "colluder77", "griffin7315", "vaultboi69", "donkeykong"]
#for i in contacts:
#    listbox.insert(END, i)

listbox.config(yscrollcommand=listscroll.set, selectmode=SINGLE)
listscroll.config(command=listbox.yview)
# ------------------------------------------------------------------------------
profilebar = Frame(top)
profilebar.place(x=222, y=0, width=958, height=50)
# ------------------------------------------------------------------------------
displayScroll = Scrollbar(top)
displayScroll.place(x=1180, y=51, width=20, height=651)

displayArea = Text(top)

displayArea.place(x=222, y=51, width=958, height=651)

displayArea.config(yscrollcommand=displayScroll.set)
displayScroll.config(command=displayArea.yview)
# ------------------------------------------------------------------------------
inputScroll = Scrollbar(top)
inputScroll.place(x=992, y=710, width=20, height=80)

inputArea = Text(top)
inputArea.insert(INSERT, "Type your message here...")
inputArea.place(x=222, y=710, width=770, height=80)

inputArea.config(yscrollcommand=inputScroll.set)
inputScroll.config(command=inputArea.yview)
# ------------------------------------------------------------------------------
send_button = tk.Button(top, text="Send", command=send)
send_button.place(x=1060, y=732, width=80, height=35)
# ------------------------------------------------------------------------------
name = "colluder77"
col = (len(name) * 0.1) + 1
message = "yo"
output = name + ":    " + message
displayArea.insert(INSERT, output)
displayArea.tag_add("name", "1.0", col)
displayArea.tag_config("name", foreground="green")
name = "griffin7315"
col = (len(name) * 0.1) + 2
message = "yes ou poon?"
output = "\n" + name + ":    " + message
displayArea.insert(INSERT, output)
displayArea.tag_add("name2", "2.0", col)
displayArea.tag_config("name2", foreground="blue")

top.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()
