import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class Server extends Thread {
	// constants
	public static int SERVER_PORT = 8000;
	
	// attributes
	private static ArrayList<BufferedWriter> clients;
	private static ServerSocket serverSocket;
	private Socket clientSocket; 
	private InputStream in; 
	private InputStreamReader inr; 
	private BufferedReader bfr;

	public Server(Socket clientSocket){ 
		this.clientSocket = clientSocket; 
		try { 
			in = clientSocket.getInputStream(); 
			inr = new InputStreamReader(in); 
			bfr = new BufferedReader(inr); 
		} catch (IOException e) { 
			e.printStackTrace(); 
		} 
	} 

	public static void main(String[] args) {
		
		Packet pack = new Packet(2, new User("Annika", "12345"), new User("Gerrie", "78910"), "Hello!");
		String ser = pack.serialize();
		
		System.out.println(ser);
		
		Packet pack2 = new Packet(ser);
		//System.out.println(pack2.serialize());
		
		/**try{
			serverSocket = new ServerSocket(SERVER_PORT); 
			clients = new ArrayList<BufferedWriter>();
			
			while(true){ 
				System.out.println("Waiting for connection..."); 
				Socket clientSocket = serverSocket.accept(); 
				System.out.println("Client connected..."); 
				Thread t = new Server(clientSocket); 
				t.start(); 
			}
			
		} catch (Exception e) { 
			e.printStackTrace(); 
		} */
	}
	
	
	public void run() {
		try {
			String msg;
		    OutputStream out = this.clientSocket.getOutputStream();
			Writer w = new OutputStreamWriter(out); 
			BufferedWriter bfw = new BufferedWriter(w); 
			clients.add(bfw); 
			msg = bfr.readLine();
		} catch (Exception e) { 
			e.printStackTrace(); 
		} 
	}
	
}
