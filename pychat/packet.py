import pickle

CODE_ERROR = 0

class Packet:
    def __init__(self, msg_code, sender, recipient, text, attachment="none"):
        self.msg_code = msg_code
        self.sender = sender
        self.recipient = recipient
        self.text = text
        self.attachment = attachment

    def serialize(self):
        return pickle.dumps(self, -1)

    @classmethod
    def deserialize(cls, serial):
        pack = pickle.loads(serial)

        return cls(pack.msg_code, pack.sender, pack.recipient, pack.text, pack.attachment)

    def __str__(self):
        return """
        msg_code:   {0}
        sender:     {1}
        recipient:  {2}
        text:       {3}
        attachment: {4}
        ---------------------------------
        """.format(self.msg_code, self.sender, self.recipient, self.text, self.attachment)

    # @property?

# sender = ("annika", "123.45.32.11")
# recipient = ("gerrie", "773.34.21.43")
# msg1 = Packet(1, sender, recipient, "Hello, Gerrie!")
# print msg1
#
# ser = msg1.serialize()
# msg2 = Packet.deserialize(ser)
#
# print msg2
