import Tkinter as tk
from Tkinter import *
from socket import AF_INET, socket, SOCK_STREAM
from threading import Event, Thread
from packet import Packet
import time
import sys

ADDR = ('localhost', 8000)
SERVER_USER = ("server", ADDR)
BUFSIZ = 1024
client_socket = socket(AF_INET, SOCK_STREAM)
username = "none"
USER = (username, "0.0.0.0")

CODE_ERROR_LOGIN = 0
CODE_PLAIN_MSG = 1
CODE_ATTACHMENT_MSG = 2
CODE_DISCONNECT = 3
CODE_LOGIN_REQUEST = 4
CODE_LOGIN_SUCCESS  = 5
CODE_USER_LOGIN = 6
CODE_USER_LOGOUT = 7

active_users = {}
running = True

def receive():
    global running

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

		displayArea.insert(INSERT, "Welcome, {0}!\n".format(username))
		displayArea.tag_add("welcome", "1.0", "1.8")
		displayArea.tag_config("welcome", foreground="green")
		displayArea.tag_add("text", "2.0", "2.0")
		displayArea.tag_config("text", foreground="blue")

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

            elif code == CODE_DISCONNECT:
                displayArea.insert(END, packet.text)
                client_socket.close()
		time.sleep(0.5)  #to see the logout message
		top.destroy()
		running = False
                break
        except OSError:  # Possibly client has left the chat.
            break

def read_msg(packet, attachment=False):
    sender = packet.sender[0]
    msg = packet.text
    disp = "{0} : {1}\n".format(sender, msg)
    displayArea.insert(END, disp)

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
    global active_users
    active_users = {}
    users = s.split("%")
    for user in users:
	uname = user.split("@")[0]
	addr = user.split("@")[1]
	active_users[uname] = addr
        #print uname, addr


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

    while running:	
        pass

    sys.exit(0)


### GUI binding ###

def repop_users():
    global active_users
    
    listbox.delete(0,'end')
    for user in active_users.iterkeys():
	if not user == USER[0]:
	    listbox.insert(END, user)

def btn_send(event=None):
    msg = inputArea.get("1.0",'end-1c')
    rec = listbox.get(listbox.curselection())

    disp = "{0} : {1}\n".format(USER[0], msg)
    displayArea.insert(END, disp)

    send(CODE_PLAIN_MSG, (rec, active_users[rec]), msg)

def on_closing(event=None):
    send(CODE_DISCONNECT, SERVER_USER, username)
    return

### elements ###
top = tk.Tk()
top.title("Chatter")
top.resizable(0,0)
top.geometry("1200x800")
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
send_button = tk.Button(top, text="Send", command=btn_send)
send_button.place(x=1060, y=732, width=80, height=35)
# ------------------------------------------------------------------------------

top.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()
