// Created by Xu Wu

import java.util.HashMap;
import java.util.*;

public class ExacDedupDB{
	private HashMap<String,MD5> dedup_db;
	private int deduplicate_count;
	public ExacDedupDB(){
		deduplicate_count=0;
		dedup_db=new HashMap<String,MD5>();
	}


	public void dedup_validation(MD5 md5){
		String md_key=md5.hash();
		if(dedup_db.containsKey(md_key)){
			deduplicate_count++;
			System.out.println("Orignal Url: "+dedup_db.get(md_key).url);
			System.out.println("Duplicate Url: "+md5.url);
			System.out.println("====== Duplicate Found :"+deduplicate_count+"======");
			return;
		}
		else{
			dedup_db.put(md_key,md5);
		}
		return;
	}

	public int getCount(){
		return deduplicate_count;
	}

}