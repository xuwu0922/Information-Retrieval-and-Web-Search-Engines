// Created by Xu Wu and Yu-tong Lee

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.FileReader;
import java.util.ArrayList;

// class Record{
//     public String url = null;
//     public String parseText = null;
//     public String metadata = null;

//     public Record(String _url, String _parseMetaData, String _parseText) {
//         url = _url;
//         metadata = _parseMetaData;
//         parseText = _parseText;
//     }
// }
/**
 * Created by hsinpailee on 10/13/15.
 */
public class NearDedupApp {
    public static void main(String[] args) throws IOException {
        
        String input_txt_path=args[0];
        ArrayList<Record> arr = new ArrayList<Record>();
        BufferedReader br = new BufferedReader(new FileReader(input_txt_path));
        String line = null;
        StringBuilder url = new StringBuilder();
        StringBuilder metadata = new StringBuilder();
        StringBuilder text = new StringBuilder();
        int count=1;
        int flag=0;
        while((line = br.readLine()) != null) {
            // do something with line.

            if (line.indexOf("url*:") != -1) {
                url.append(line);flag=1;
            }
            else if(line.indexOf("metadata*:") != -1){
                metadata.append(line);flag=2;
            }
            else if(line.indexOf("text*:") != -1){
                text.append(line);flag=3;
            }
            else if(line.indexOf("*=*=*=") != -1){
                Record record = new Record(url.toString().substring(5),metadata.toString().substring(10),text.toString().substring(6));
                arr.add(record);
                url.setLength(0);
                metadata.setLength(0);
                text.setLength(0);
            }
            else{
                if(flag==2)
                    metadata.append(line);
                else if(flag==3)
                    text.append(line);
            }
        }
        // System.out.println(arr.size());
        // for(int i=0;i<arr.size();i++){
        //     System.out.println(arr.get(i).url);
        //     System.out.println(arr.get(i).metadata);
        //     System.out.println(arr.get(i).parseText);

        //     System.out.println("====================================");
        // }
        br.close();
        DedupDB simHashMap = new DedupDB();
        for(int i=0;i<arr.size();i++){
            if(arr.get(i).metadata!=" "||arr.get(i).parseText!=" "){
                System.out.println("Url: " + arr.get(i).url);
                SimHash simhash= new SimHash(arr.get(i),64);
                simHashMap.dedup_validation(simhash);


            }

        }
    }


}
