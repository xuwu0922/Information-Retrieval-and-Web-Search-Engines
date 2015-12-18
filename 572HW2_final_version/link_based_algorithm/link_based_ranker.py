# created by Xu Wu and Longpeng Jiao

import networkx as nx
import node as nd
import os
import sys
import json
import itertools
import codecs
from sets import Set
import math
reload(sys) 
sys.setdefaultencoding('UTF8')

def caculate_distance(lst1,lst2):
	if len(lst1)!=len(lst2):
		return 0
	dist_sum=0
	for i in range(len(lst1)):
		dist_sum = dist_sum + (lst1[i]-lst2[i])**2
	return math.sqrt(dist_sum)

def compute_page_rank(graph, d=0.85, delta=0.2):

	dst = 1
	while dst > delta:
		old_vec =[]
		new_vec = []
		for node in graph.nodes():
			_compute_page_score(node, d, old_vec, new_vec)
		dst = caculate_distance(old_vec, new_vec)
		print 'new dst = ' + str(dst)

	return graph


def _compute_page_score(node, d, old_vec, new_vec):
	fractions = 0 
	for neigh in node.neighbors:
		new_ratio = neigh.linkScore/neigh.noLinks
		fractions = fractions + new_ratio

	new_score = (1-d) + d*fractions
	old_vec.append(node.linkScore)
	node.linkScore = new_score
	new_vec.append(new_score)



def getAttr(attr,node,keywords_list):
	if attr=="description":
		if len(keywords_list)==0:
			return [node.description]

		else:
			for keyword in keywords_list:
				print "keyword:",keyword
				print "nodddd:", node.nodeId,node.contain_key
				if node.description.lower().find(keyword)!=-1:
				# descr="contain"
					if keyword not in node.contain_key:
						node.contain_key=node.contain_key+[keyword]
					# node.contain_key.append(keyword)
						print node.nodeId,node.contain_key
				else:
					continue
			
			if node.contain_key==[]:
				descr=["not_contain"]
				return descr
			else:
				return node.contain_key
	else:
		str=node.location.split(',')
		if len(str)==3:
			node_location=str[1]
		else:
			node_location=str[0]

		return{
			"nodeId":[node.nodeId],
			"location":[node_location],
			"country":[node.country],
			"title":[node.title],
			"sellerDesc":[node.sellerDesc],
			"sellerStartDate":[node.sellerStartDate],
			"postUrl":[node.postUrl],
			"availableDate":[node.availableDate],
			"itemCategory":[node.itemCategory],
			"itemKeywords":[node.itemKeywords],
			"itemManufacturer":[node.itemManufacturer],
			"linkScore":[node.linkScore],
			"noLinks":[node.noLinks],
			"neighbors":[node.neighbors]
		}[attr]

def printAttr(attr,node):
		return{
		"nodeId":node.nodeId,
		"location":node.location,
		"country":node.country,
		"title":node.title,
		"description":node.description,
		"sellerDesc":node.sellerDesc,
		"sellerStartDate":node.sellerStartDate,
		"postUrl":node.postUrl,
		"availableDate":node.availableDate,
		"itemCategory":node.itemCategory,
		"itemKeywords":node.itemKeywords,
		"itemManufacturer":node.itemManufacturer,
		"linkScore":node.linkScore,
		"noLinks":node.noLinks,
		"neighbors":node.neighbors
	}[attr]


# argvList=sys.argv[2:]
argvList=sys.argv[3:]
file_path=sys.argv[1]
keywords_list=eval(sys.argv[2])
G=nx.Graph()
Files=os.listdir(file_path)
for afile in Files:
	if afile==".DS_store":
		continue
	else:
		curFilePath="{0}/{1}".format(file_path, afile)
		# curFilePath='./90001.json'
		jsonFile=open(curFilePath,'r')
		aJson=json.load(jsonFile)
		# node=nd.Node()
		node=nd.getNodeFromJson(aJson)
		G.add_node(node)
		print G.number_of_nodes()
		print "============="
		print curFilePath
		print node.nodeId
		print "**************************************"
		jsonFile.close()

print argvList



# store the nodes into hash_map
hash_map={}
for attr in argvList:
	hash_map[attr]={}
	for node in G.nodes():
		content_list=getAttr(attr,node,keywords_list)
		for content in content_list:
			if content!="not_contain" and content!="1900-01-01 00:00:00" and content!="" and content!=" ":
				print content
				print "***************************************"
				if content in hash_map[attr]:
					hash_map[attr][content].add(node)
				else:
					hash_map[attr][content]=Set([node])

# for attr in hash_map:
# 	for content in hash_map[attr]:
# 		for node in 

for node in G.nodes():
	print "...processing nodeId:",node.nodeId
	for attr in hash_map:
		for content in hash_map[attr]:
			if node in hash_map[attr][content]:
				node.noLinks+=(len(hash_map[attr][content])-1)
				node.neighbors=node.neighbors|hash_map[attr][content]
	if node in node.neighbors:
		node.neighbors.remove(node)

# for node in G.nodes():
# 	print node.nodeId
# 	print "description:", node.description
# 	print node.noLinks
# 	print node.neighbors
# 	print "===================================="

# # link the graph, store num of earh pair of nodes (i,j) into G[i][j]["num"]
# for attr in hash_map:
# 	for content in hash_map[attr]:
# 		for node in hash_map[attr][content]:
# 			nd_index=hash_map[attr][content].index(node)
# 			for node2 in hash_map[attr][content][nd_index+1:]:
# 				if node2 not in G.neighbors(node):
# 					G.add_edge(node,node2,num=1)
# 				else:
# 				 	G[node][node2]["num"]=G[node][node2]["num"]+1
# 				print "^^^^^^^^^^^^^^^^^^^^^"
# 				print G[node][node2]["num"]
# 				print "^^^^^^^^^^^^^^^^^^^^^"

# # test the num of edges
# for edge in G.edges():
# 	print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
# 	print edge[0].nodeId,edge[1].nodeId
# 	print edge
# 	print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"

# # test the num of links for each node and store it in node.noLinks
# for node in G.nodes():
# 	print G.neighbors(node)
# 	if len(G.neighbors(node))!=0:
# 		for neigh in G.neighbors(node):
# 			node.noLinks=node.noLinks+G[node][neigh]["num"]
# 	print "links of node:",node.nodeId,"-->",node.noLinks

scored_graph = compute_page_rank(G)

'''
for i in range(scored_graph.number_of_nodes()):
	node_i=scored_graph.nodes()[i]
	print 'node'+str(i)+'score = '+str(node_i.linkScore)
'''

f1=codecs.open("4b.txt","w",encoding='utf8')

lstscore=[]
print "======all node score========="
low_scoring = []
for node in G.nodes():
	#print node.nodeId,node.linkScore
	lstscore.append(node)
	if len(low_scoring)<20 and node.linkScore<0.3:
		low_scoring = low_scoring + [node]
print "==========sorted=========="
lstscore.sort(key=lambda node: node.linkScore, reverse=True)
for node in lstscore[:50]:
	str1="nodeId: "+node.nodeId+'\nscore: '+str(node.linkScore)+'\n'
	for attr in argvList:
		str1+=attr+": "+printAttr(attr,node)+'\n'
	f1.write(str1+'\n')
f1.write('==========low scoring======')
for node in low_scoring:
	str1="nodeId: "+node.nodeId+'\nscore: '+str(node.linkScore)+'\n'
	for attr in argvList:
		str1+=attr+": "+printAttr(attr,node)+'\n'
	f1.write(str1+'\n')
	
f1.close()


