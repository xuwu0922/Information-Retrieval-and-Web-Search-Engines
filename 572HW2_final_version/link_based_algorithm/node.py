import datetime
import os
import sys
import json
from sets import Set

class Node(object):
	nodeId = ''
	location =''
	country=''
	title =''
	description=''
	sellerDesc=''
	sellerStartDate=''
	postUrl=''
	availableDate=''
	itemCategory=''
	itemKeywords=''
	itemManufacturer=''
	linkScore=0.5
	noLinks=0
	neighbors=Set([])
	contain_key=[]

	def __init__(self, nodeId, location, country, title, description, sellerDesc, sellerStartDate, postUrl, 
					availableDate, itemCategory, itemKeywords, itemManufacturer, linkScore=0.5, noLinks=0, neighbors=Set([]),contain_key=[]):
		self.nodeId = nodeId
		self.location = location
		self.title = title
		self.description = description
		self.sellerDesc = sellerDesc
		self.sellerStartDate = sellerStartDate
		self.postUrl = postUrl
		self.availableDate = availableDate
		self.itemCategory = itemCategory
		self.itemKeywords = itemKeywords
		self.itemManufacturer = itemManufacturer
		self.linkScore=linkScore
		self.noLinks=noLinks
		self.neighbors=neighbors
		self.contain_key=contain_key

def getNodeFromJson(aJson):
	'''
	Extracts field values from json and return a node object with assigned object variables
	'''

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

	if 'title' in aJson:
		title= aJson["title"]
	else:
		title =''
	
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

	newNode = _make_node(title, location, country, title, description, sellerDesc, sellerStartDate, postUrl, 
					availableDate, itemCategory, itemKeywords, itemManufacturer, 0)
	return newNode



def _make_node(nodeId, location, country, title, description, sellerDesc, sellerStartDate, postUrl, 
					availableDate, itemCategory, itemKeywords, itemManufacturer, linkScore=0.5, noLinks=0, neighbors=Set([]),contain_key=[]):
	node = Node(nodeId, location, country, title, description, sellerDesc, sellerStartDate, postUrl, 
					availableDate, itemCategory, itemKeywords, itemManufacturer, linkScore, noLinks, neighbors,contain_key)
	return node


def add_neighbor(node, neighbor):
	node.neighbors.append(neighbor)



# def main():

# 	'''
# 	Main as example usage of node
# 	'''
# 	curFilePath='./30194.json'
# 	jsonFile = open(curFilePath, 'r')
# 	aJson = json.load(jsonFile)

# 	node = getNodeFromJson(aJson)

# 	print node.description



# if __name__ == '__main__':
#     main()
# else:
#     print("Node loaded as a module")

