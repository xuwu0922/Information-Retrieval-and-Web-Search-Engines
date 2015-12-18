import os
import sys
reload(sys) 
import tika
import elasticsearch
from tika import parser


host = 'search-csci572-vbd7idisazj5dy44rsanqhhtkq.us-west-2.es.amazonaws.com'

#es = elasticsearch.Elasticsearch()
es = elasticsearch.Elasticsearch(hosts=[{'host': host, 'port': 80}], http_auth=None, use_ssl=False, verify_certs=False, ca_certs=None, client_cert=None, connection_class=elasticsearch.connection.RequestsHttpConnection)

newIndexName = 'json_weapons_index'
newDocType = 'weapon_doc'

es.indices.create(
        index=newIndexName,
        body={
          'settings': {
            'number_of_shards': 5,
            'number_of_replicas': 1
            }
        	},
        ignore=400
        )

weapon_doc_mapping={
	newDocType:{
		'properties':{
			'location':{'type':'string'},
			'country':{'type':'string', "index": "not_analyzed"},
			'price':{'type':'string', "index": "not_analyzed"},
			'title':{'type':'string'},
			'publisherName':{'type':'string', "index": "not_analyzed"},
			'orgName':{'type':'string', "index": "not_analyzed"},
			'description':{'type':'string'},
			'sellerDesc':{'type':'string', "index": "not_analyzed"},
			'sellerStartDate':{'type':'date', "format": "yyyy-MM-dd HH:mm:ss || yyyy-MM-dd", "index": "not_analyzed"},
			'postUrl':{'type':'string', "index": "not_analyzed", "index": "not_analyzed"},
			'availableDate':{'type':'date', "format": "yyyy-MM-dd HH:mm:ss || yyyy-MM-dd", "index": "not_analyzed"},
			'itemCategory':{'type':'string'},
			'itemKeywords':{'type':'string'},
			'itemManufacturer':{'type':'string'},
			'linkScore':{'type':'double'}
		}
	}
}
'''
	Send new index and mappping to elasticsearch instance on aws
'''
es.indices.put_mapping(index=newIndexName, doc_type='weapon_doc', body=weapon_doc_mapping)

print "Created new Index: " + newIndexName + " and assigned mapping for "+ newDocType






#print res