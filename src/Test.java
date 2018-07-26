public class Test {
    public static void main(String[] args) {
        Packet pack = new Packet(2, new User("Annika", "12345"), new User("Gerrie", "78910"), "Hello!");
        System.out.println(pack);

        //String ser = pack.serialize();
        //System.out.println(ser);

        Packet pack2 = new Packet(pack.toString());
        System.out.println(pack2);

    }


}
