# Game Plan

Client/Server chatroom in Java.

Use the following link as a guide: [Creating a Multithreaded Chat with Socket in Java](http://mrbool.com/creating-a-multithreaded-chat-with-socket-in-java/34275)

## Server

* `Server.java` extends `Thread`
* Use built-in `ServerSocket` class
* Multithreaded Server: listen for connection and fork new thread for each new connection, which in turn listens for messages from the client.
* Contains `ArrayList` of logged on clients. Client nicknames must be distinct.
	- `User` object containing: username, ip

## Client

* Use `Socket` class.
* GUI that reacts differently to different message types.
* Processes:
	- main - detects user input and sends messages to server. Loops while logged in.
	- listener thread - listens to message from the server and reacts accordingly. Loops while logged in.

## Message passing

* Create `Packet` class that contains:
	- int msgCode (1 = Login, 2 = Logout, 3 = TextMessage, 4 = Picture)
	- User sender (who sent the message?)
	- User recipient (to whom must the message be sent; NULL for server messages e.g. login/logout)
	- String text (actual message to send)
	- Image attachment (picture to send; bytestream?)

* Serialize `Packet` before and send String to server, where server **deserializes** packet to build object. Then interprets object accordingly.
* Similarly, packets from server are serialized and sent to clients.

## TODO

### Annika

1. Figure out deserialization using gson
2. Basic client server test
3. Implement threading
4. Mutexes

### Gerrie

1. Make GUI
2. ?
