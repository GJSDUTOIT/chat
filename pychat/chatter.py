import Tkinter as tk
from Tkinter import *

def send(event=None):
    print('hi')

def on_closing(event=None):
    return

top = tk.Tk()
top.title("Chatter")
top.resizable(0,0)
top.geometry("1200x800")
# ------------------------------------------------------------------------------
listscroll = Scrollbar(top)
listscroll.place(x=201, y=0, width=20, height=800)

listbox = Listbox(top)
listbox.place(x=0, y=0, width=200, height=800)
contacts = ["Chat Room", "colluder77", "griffin7315", "vaultboi69", "donkeykong"]
for i in contacts:
    listbox.insert(END, i)

listbox.config(yscrollcommand=listscroll.set)
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
inputArea.insert(INSERT, "Type your message here.........")
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
