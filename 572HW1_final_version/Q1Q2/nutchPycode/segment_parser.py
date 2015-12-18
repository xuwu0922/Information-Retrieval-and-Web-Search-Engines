

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
import nutchpy

file_name = sys.argv[1]
outfile_name = sys.argv[2]
node_path = file_name
seq_reader = nutchpy.sequence_reader
data = seq_reader.read(node_path)
totUrls = seq_reader.count(node_path)
mimeCount = {}
status={}
images=0;

text_file=open(outfile_name, "w")
text_file.write("Total number of urls: %d" % totUrls)
for url in data:
	text_file.write("\n\nCrawl data for %s" % url[0])
	url_i = url[0];
	list_len = len(url)
	for i in range(1, list_len):
		tag = url[i]
		mime=""
		status_i=""
		
		if tag.find("Status:")!=-1:
			end = tag.find(")", 9, 40)
			status_i=tag[10:end+1]
			if status_i in status:
				status[status_i] = status[status_i]+1
			else:
				
				status[status_i]=1

		if tag.find("Metadata")!=-1:
			index=0
			index=tag.find("Content-Type")
			if(index!=-1):
				index+=13
				end = tag.find("\n", index)
				mime=tag[index:end]
				if(mime.find("image")!=-1):
					images=images+1
				if mime in mimeCount:
					mimeCount[mime] = mimeCount[mime]+1
				else:
					mimeCount[mime] = 1

		text_file.write(url[i])



text_file.write("\n\n**********************************************STATISTICS*******************************************************\n")
text_file.write("\n\n*****MimeType Count*****\n")
text_file.write("\n\nImages Count: {0}\n\n".format(images))


for key in mimeCount:
	text_file.write("{0} ({1})\n".format(key, mimeCount[key]))


text_file.write("\n\n*****Statuses Count*****\n")
for key in status:
	text_file.write("{0} ({1})\n".format(key, status[key]))
#	text_file.write("\nURLs for status {0}:\n\n".format(key))
#	j=0
#	for aUrl in status[key]:
#		j=j+1
#		text_file.write("{0}. {1}\n".format(j, aUrl))
	
text_file.close();



#print(seq_reader.read(node_path))
#print(seq_reader.slice(10,20,node_path))