

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
import nutchpy

#data_path = "/Users/longpengjiao/Desktop/cs572/nutch/runtime/local/crawl/segments/20151014015520/parse_data/part-00000/data"
#text_path = "/Users/longpengjiao/Desktop/cs572/nutch/runtime/local/crawl/segments/20151014015520/parse_text/part-00000/data"
data_path = "/Users/xuwu/Desktop/dedupfinal/segments/20151014142205/parse_data/part-00000/data"
text_path = "/Users/xuwu/Desktop/dedupfinal/segments/20151014142205/parse_text/part-00000/data"

seq_reader = nutchpy.sequence_reader
data = seq_reader.read(data_path)
text = seq_reader.read(text_path)

urlMap = {}

text_file=open("stringsForDedup.txt", "w")
#text_file.write("Total number of urls: %d" % totUrls)

for url in data:
	#url_i = url[0];
	tag = url[1]
	length=len(tag)
	parseMetaStart = tag.find("Parse Metadata:")
	if parseMetaStart!=-1:
		startContentType=tag.find("Content-Type=", parseMetaStart)
		if startContentType!=-1:
			contentType = tag[startContentType+13: startContentType+18]
			if contentType=="image":
				urlMap[url[0]]= "metadata*: " +tag[parseMetaStart+16:length]

										
for item in text:
	url_text = item[0]
	if url_text in urlMap:
		first = urlMap[url_text]
		second = "text*: "+item[1]
		newString = first+second
		urlMap[url_text]=newString
		


for key in urlMap:
	text_file.write("{0}\n{1}\n*=*=*=\n".format("url*: "+key, urlMap[key]))
	
text_file.close();


#print(seq_reader.read(node_path))
#print(seq_reader.slice(10,20,node_path))