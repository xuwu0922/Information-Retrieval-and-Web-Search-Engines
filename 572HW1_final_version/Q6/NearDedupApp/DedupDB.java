// Created by Xu Wu

import java.math.BigInteger;  
import java.util.ArrayList;  
import java.util.List;  
import java.util.HashMap;
import java.util.*;

public class DedupDB{
	private ArrayList<HashMap<BigInteger,ArrayList<SimHash>>> simhash_db=new ArrayList<HashMap<BigInteger,ArrayList<SimHash>>>();
	private int distance;
	private int duplicate_count;
	public DedupDB(){
		distance=3;
		duplicate_count=0;
		// simhash_db=new ArrayList<HashMap<BigInteger,ArrayList<SimHash>>>();
		for(int i=0;i<distance+1;i++){
			HashMap<BigInteger,ArrayList<SimHash>> map=new HashMap<BigInteger,ArrayList<SimHash>>();
			simhash_db.add(map);
		}	
	}

	public void dedup_validation(SimHash simhash){
		List<BigInteger> index_group=simhash.subByDistance(simhash,this.distance);
		for(int i=0;i<index_group.size();i++){
			BigInteger bigkey=index_group.get(i);
			if(simhash_db.get(i).containsKey(bigkey)){
				ArrayList<SimHash> tmp=simhash_db.get(i).get(bigkey);
				for(int j=0;j<tmp.size();j++){
					if(simhash.hammingDistance(tmp.get(j))<=this.distance){
						duplicate_count++;
						System.out.println("Orignal Url: "+tmp.get(j).url);
						System.out.println("Duplicate Url: "+simhash.url);
						System.out.println("====== Duplicate Found :"+duplicate_count+" =======");
						return;
						// return true;
					}
				}
				simhash_db.get(i).get(bigkey).add(simhash);
				// return false;
			}
			else{
				ArrayList<SimHash> new_keylist = new ArrayList<SimHash>();
				new_keylist.add(simhash);
				simhash_db.get(i).put(bigkey,new_keylist);
				// return false;
			}
		}
	}

	public int getCount(){
		return duplicate_count;
	}
}