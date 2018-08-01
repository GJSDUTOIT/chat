import Tkinter as tk
from Tkinter import *

iniFrame = tk.Tk()
iniFrame.geometry("250x320")
iniFrame.resizable(0,0)
iniFrame.title("Chatter")

#def open:
#    self.iniFrame.destroy()
# ------------------------------------------------------------------------------
var = StringVar()
label = Label(iniFrame, textvariable=var)
var.set("Host:")
label.place(x=20, y=90, width=40, height=20)
host = Text(iniFrame)
host.place(x=70, y=90, width=150, height=20)

var2 = StringVar()
label2 = Label(iniFrame, textvariable=var2)
var2.set("Port:")
label2.place(x=20, y=130, width=40, height=20)
port = Text(iniFrame)
port.place(x=70, y=130, width=90, height=20)
#-------------------------------------------------------------------------------
var3 = StringVar()
label3 = Label(iniFrame, textvariable=var3)
var3.set("Error: invalid host")
#label3.place(x=0, y=170, width=240, height=20)
#-------------------------------------------------------------------------------
connect = tk.Button(iniFrame, text="Connect", command=open)
connect.place(x=90, y=200, width=80, height=35)
#-------------------------------------------------------------------------------
iniFrame.mainloop()
