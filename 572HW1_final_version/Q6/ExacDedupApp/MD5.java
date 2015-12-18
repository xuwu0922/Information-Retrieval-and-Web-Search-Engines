import java.security.*;
import java.lang.StringBuilder;

public class MD5{
	private String s;
	public String url;
	public MD5(Record tokens){
		StringBuilder str=new StringBuilder();
        str.append(tokens.metadata);
        str.append(tokens.parseText);    
        s = str.toString(); 
		url=tokens.url;

	}

	public String hash(){
		StringBuilder res = new StringBuilder();
try{
		MessageDigest md = MessageDigest.getInstance("MD5");
		byte[] toByte =s.getBytes();
		md.update(toByte);
		byte[] toHex_byte=md.digest();
		for(int i=0;i<toHex_byte.length;i++){
			String temp=Integer.toHexString(toHex_byte[i]&0xFF);
			if(temp.length()!=1){
				res.append(temp);
			}
			else{
				res.append('0');
			}
			
		}
		
	}
catch (NoSuchAlgorithmException e) {
	System.out.println("No Such Algorithm");
	}	
	return res.toString();
}

}