package chat;

public class User {
	private String username;
	private String ip;
	
	public User(String username, String ip) {
		this.username = username;
		this.ip = ip;
	}
	
	public String getUsername() {
		return this.username;
	}
	
	public String getIp() {
		return this.ip;
	}
}
