#!/usr/bin/env python2.7
'''
	Python script to extract metadata and content from dumped out files and index them to elasticsearch

	NOTE: before running this script, need to have tika-servers for normal parsing and geo-data parsing as described in readme
		  as well as awsEsTikaIndexCreate.py so that index and doc type mapping are setup

	'normal' Tika server on default http://localhost:9998/
	'geo' 	 Tika server on http://localhost:9997/
'''
import tika
from tika import parser
import os
import sys
reload(sys) 
sys.setdefaultencoding('UTF8')
import elasticsearch

host = 'search-csci572-vbd7idisazj5dy44rsanqhhtkq.us-west-2.es.amazonaws.com'
es = elasticsearch.Elasticsearch(hosts=[{'host': host, 'port': 80}], http_auth=None, use_ssl=False, verify_certs=False, ca_certs=None, client_cert=None, connection_class=elasticsearch.connection.RequestsHttpConnection)


file_path = sys.argv[1]

#outfile_name = sys.argv[2]

for aFile in os.listdir(file_path):
	if aFile == '.DS_Store':
		continue

	curFilePath = "{0}/{1}".format(file_path, aFile)
	'''
		Use tika-server to get parsed metadata and content, server at localhost:9998 does not include NER enchancements
	'''
	parsedData = parser.from_file(curFilePath, 'http://localhost:9998/tika')
	if 'metadata' in parsedData:
		metadata = parsedData['metadata']
		if 'Content-Type' in metadata:
			content_type = metadata['Content-Type']
			content_type = content_type.split(';')[0]
		else:
			content_type =''
		if 'description' in metadata:
			description=metadata['description']
		else:
			description=''
		if 'keywords' in metadata:
			itemKeywords=metadata['keywords']
		else:
			itemKeywords=''
		if 'title' in metadata:
			title=metadata['title']
		else:
			title=''
		'''
			this will only be extracted if file is image type
		'''
		if 'Date/Time Original' in metadata:
			postDate = metadata['Date/Time Original']
		else 
			postDate =''
	else:
		content_type = ''
		description=''
		itemKeywords=''
		title=''

	'''
		use tika-server to get content in plain text. A new .geot file is created with contents in plain text, which will be sent to tika-server with geo-parsing
		capabilitites to extract geo related metadata
	'''
	textResponse = parser.parse1('text', curFilePath)
	if not textResponse:
		parsedText =''
	else:
		parsedText = textResponse[1]

	'''
		to parse out 'posted date' of gun ads for ad if we are dealing with html pages
	'''
	if postDate == '':
		postDateStart = parsedText.find('Posted')
		if(postDateStart!=-1):
			postDate = parsedText[postDateStart+8:postDateStart+40]
		else:
			postDate = '1900-01-01 00:00:00'
	else 	
		postDate = '1900-01-01 00:00:00'
		
	'''
		make new .geot file with parsed out text from files
	'''
	fileName = aFile.split('.')[0]
	newGeoFileName=fileName+'.geot'
	newGeoFile = open(newGeoFileName, 'w')
	newGeoFile.write(parsedText)
	newGeoFile.close()
	'''
		send new .geot file to tika-server with geo-parsing capabilitites to obtain geo data at localhost:9997
	'''
	parsedGeo = parser.from_file('./'+newGeoFileName, 'http://localhost:9997/rmeta --header "Content-type: application/geotopic"')
	if 'metadata' in parsedGeo and 'Geographic_NAME' in parsedGeo['metadata']:
		location = parsedGeo['metadata']['Geographic_NAME']
	else:
		location = ''


	'''
		create json that and include the extracted values for the fields needed for indexing
	'''
	doc_data = {
		'resourceName':fileName,
		'contentType':content_type,
		'description':description,
		'itemKeywords':itemKeywords,
		'title':title,
		'date':postDate,
		'location':location,
		'content':parsedText,
		'linkScore':0

	}

	'''
		Call elasticsearchpy indexing api and pass in indexing data for file
	'''
	res = es.index(index="weapons_tika_index", doc_type='weapon_doc', id=fileName, body=doc_data)
	print 'Indexing '+ fileName + ' into weapons_tika_index, indexed: '+str(res['created'])+'.'

print 'Finished indexing!!!!'




	














