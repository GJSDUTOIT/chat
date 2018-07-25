
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
	private Image attachment;
	private Gson gson;
	
	public Packet(int msgCode, User sender, User recipient, String text) {
		super();
		this.msgCode = msgCode;
		this.sender = sender;
		this.recipient = recipient;
		this.text = text;
		this.attachment = null;
		
	}
	
	public Packet(int msgCode, User sender, User recipient, String text, Image attachment) {
		super();
		this.msgCode = msgCode;
		this.sender = sender;
		this.recipient = recipient;
		this.text = text;
		this.attachment = attachment;
	}

	public Packet(String serial) {
		// deserialize
		Packet pack = gson.fromJson(serial, Packet.class);
		
		// build object
		this.msgCode = pack.msgCode;
		this.sender = pack.sender;
		this.recipient = pack.recipient;
		this.text = pack.text;
		this.attachment = pack.attachment;
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
	
	public Image getAttachment() {
		return attachment;
	}
	
	public void setAttachment(Image attachment) {
		this.attachment = attachment;
	}
	
	public String serialize() {
		
		// create gson builder
		gson = new GsonBuilder().create();
		
		String serial = gson.toJson(this);
		return serial;
		
	}
}
