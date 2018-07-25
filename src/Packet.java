
import java.awt.Image;
import java.io.Serializable;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

// GJSON library: https://github.com/google/gson

public class Packet implements Serializable {
	private int msgCode;
	private User sender;
	private User recipient;
	private String text;
	//private Image attachment;
	private String attachment;
	private Gson gson;
	
	public Packet(int msgCode, User sender, User recipient, String text) {
		super();
		this.msgCode = msgCode;
		this.sender = sender;
		this.recipient = recipient;
		this.text = text;
		this.attachment = "none";
		
	}
	
	public Packet(int msgCode, User sender, User recipient, String text, String attachment) {
		super();
		this.msgCode = msgCode;
		this.sender = sender;
		this.recipient = recipient;
		this.text = text;
		this.attachment = attachment;
	}

	/*
	public Packet(String serial) {
		gson = new Gson();
		Packet pack = gson.fromJson(serial, Packet.class);

		this.msgCode = pack.msgCode;
		this.sender = pack.sender;
		this.recipient = pack.recipient;
		this.text = pack.text;
		this.attachment = pack.attachment;
	}*/


	public Packet(String serial) {
		int index;

		// reconstruct object

		// msgCode
		index = serial.indexOf("\"msgCode\":\"");
		this.msgCode = Integer.parseInt(serial.substring(index, serial.indexOf("\"", index)));

		// text
		index = serial.indexOf("\"text\":\"");
		this.text = serial.substring(index, serial.indexOf("\"", index));

		// attachment
		index = serial.indexOf("\"attachment\":\"");
		this.attachment = serial.substring(index, serial.indexOf("\"", index));

		// sender
		index = serial.indexOf("\"sender\":User ");
		String senderJSON = serial.substring()
	}
	
	public int getMsgCode() {
		return msgCode;
	}
	
	public void setMsgCode(int msgCode) {
		this.msgCode = msgCode;
	}
	
	public User getSender() {
		return sender;
	}
	
	public void setSender(User sender) {
		this.sender = sender;
	}
	
	public User getRecipient() {
		return recipient;
	}
	
	public void setRecipient(User recipient) {
		this.recipient = recipient;
	}
	
	public String getText() {
		return text;
	}
	
	public void setText(String text) {
		this.text = text;
	}
	
	public String getAttachment() {
		return attachment;
	}
	
	public void setAttachment(String attachment) {
		this.attachment = attachment;
	}

	/*
	public String serialize() {
		gson = new GsonBuilder().create();

		return gson.toJson(this);
	}*/

	@Override
	public String toString() {
		return "Packet {"
				+ "\"msgCode\":\"" + this.msgCode + "\","
				+ "\"sender\":User {"
					+ "\"username\":\"" + this.sender.getUsername() + "\","
					+ "\"ip\":\"" + this.sender.getIp() + "\"},"
				+ "\"recipient\":User {"
					+ "\"username\":\"" + this.recipient.getUsername() + "\","
					+ "\"ip\":\"" + this.recipient.getIp() + "\"},"
				+ "\"text\":\"" + this.text + "\","
				+ "\"attachment\":\"" + this.attachment + "\"}";

	}
}
