
import os
import sys
import json
import elasticsearch
reload(sys) 
sys.setdefaultencoding('UTF8')
#es = elasticsearch.Elasticsearch()

host = 'search-csci572-vbd7idisazj5dy44rsanqhhtkq.us-west-2.es.amazonaws.com'

#es = elasticsearch.Elasticsearch()
es = elasticsearch.Elasticsearch(hosts=[{'host': host, 'port': 80}], http_auth=None, use_ssl=False, verify_certs=False, ca_certs=None, client_cert=None, connection_class=elasticsearch.connection.RequestsHttpConnection)
file_path = sys.argv[1]

#outfile_name = sys.argv[2]

for aFile in os.listdir(file_path):
	if aFile == '.DS_Store':
		continue
	curFilePath = "{0}/{1}".format(file_path, aFile)
	jsonFile = open(curFilePath, 'r')
	aJson = json.load(jsonFile)

	if "availableAtOrFrom" in aJson and 'address' in aJson["availableAtOrFrom"] and 'name' in aJson["availableAtOrFrom"]['address']:
		location = aJson["availableAtOrFrom"]["address"]["name"]
	else:
		location =''
	if "description" in aJson:
		description = aJson['description']
	else:
		description =''
	if "geonames_address" in aJson and'fallsWithinCountry' in aJson["geonames_address"][0] and 'hasName' in aJson["geonames_address"][0]["fallsWithinCountry"] and 'label' in aJson["geonames_address"][0]["fallsWithinCountry"]['hasName']:
		country= aJson["geonames_address"][0]["fallsWithinCountry"]['hasName']["label"]
	else:
		country =''
	if 'price' in aJson:
		price= aJson["price"]
	else:
		price =''

	if 'title' in aJson:
		title= aJson["title"]
	else:
		title =''

	if 'publisher' in aJson and 'name' in aJson['publisher']:
		publisherName= aJson['publisher']['name']
	else:
		publisherName =''
	
	if 'seller' in aJson:
		if 'memberOf' in aJson['seller'] and 'startDate' in aJson["seller"]["memberOf"]:
			sellerStartDate=aJson["seller"]["memberOf"]['startDate'].replace('T', ' ')
			orgName=aJson["seller"]["memberOf"]["memberOf"]["name"]
		else:
			orgName=''
			sellerStartDate='1900-01-01 00:00:00'
		if	"description" in aJson["seller"]:
			sellerDesc = aJson['seller']["description"]
		else:
			sellerDesc=''
	else:
		orgName=''
		sellerDesc=''
		sellerStartDate='1900-01-01 00:00:00'

	if "availabilityStarts" in aJson:
		if len(aJson['availabilityStarts'])=='':
			availableDate='1900-01-01 00:00:00'
		else:
			availableDate=aJson['availabilityStarts'].replace('T', ' ')
	else:
		availableDate='1900-01-01 00:00:00'


	if "url" in aJson:
		postUrl = aJson["url"]
	else:
		postUrl=''

	if "itemOffered" in aJson:
		if 'category' in aJson["itemOffered"]:
			itemCategory=aJson['itemOffered']['category']
		else:
			itemCategory=''
		if "keywords" in aJson["itemOffered"]:
			itemKeywords=''
			for word in aJson['itemOffered']['keywords']:
				if len(itemKeywords)==0:
					itemKeywords += word
				else:
					itemKeywords += ' '+word
		else:
			itemKeywords=''

		if "manufacturer" in aJson["itemOffered"]:
			itemManufacturer = aJson["itemOffered"]["manufacturer"]
		else:
			itemManufacturer=''
	else:
		itemCategory=''
		itemKeywords=''
		itemManufacturer=''

	jsonFile.close()

	#print availableDate
	#print sellerStartDate

	doc = {
			'location':location,
			'country':country,
			'price':price,
			'title':title,
			'publisherName':publisherName,
			'orgName':orgName,
			'description':description,
			'sellerDesc':sellerDesc,
			'sellerStartDate':sellerStartDate,
			'postUrl':postUrl,
			'availableDate':availableDate,
			'itemCategory':itemCategory,
			'itemKeywords':itemKeywords,
			'itemManufacturer':itemManufacturer,
			'linkScore':0
	}

	fileName = aFile.split('.')[0]

	print 'id: '+fileName
	'''
		post new extracted json to elasticsearch
	'''
	res = es.index(index="json_weapons_index", doc_type='weapon_doc', id=fileName, body=doc)
	print 'Indexing '+ fileName + ' into weapons_index_metadata, indexed: '+str(res['created'])+'.\n'	

print "finished indexing!!!!!!!!!!!!!"








	


	


	
		
