import os
import sys
reload(sys) 
import elasticsearch
host = 'search-csci572-vbd7idisazj5dy44rsanqhhtkq.us-west-2.es.amazonaws.com'

newIndexName="weapons_tika_index"
newDocType="weapon_doc"

es = elasticsearch.Elasticsearch(hosts=[{'host': host, 'port': 80}], http_auth=None, use_ssl=False, verify_certs=False, ca_certs=None, client_cert=None, connection_class=elasticsearch.connection.RequestsHttpConnection)

'''
    creates new index, in this case called 'weapons_tika_index'
'''
es.indices.create(
        index=newIndexName,
        body={
          'settings': {
            # just one shard, no replicas for testing
            'number_of_shards': 5,
            'number_of_replicas': 1
            }
        	},
        ignore=400
        )

'''
    define the mapping for 'weapon_doc' doc type
'''
weapon_doc_mapping={
	newDocType:{
		'properties':{
			'resourceName':{'type':'string'},
			'contentType':{'type':'string', "index": "not_analyzed"},
			'description':{'type':'string', 'store':'true'},
            'keywords':{'type':'string', "index": "not_analyzed"},
			'title':{'type':'string'},
			'date':{'type':'string', "index": "not_analyzed"},
			'geographicName':{'type':'string', "index": "not_analyzed"},
            'content':{'type':'string'},
            'linkScore':{'type':'double'}
		}
	}
}


'''
    send mapping configuration to elasticsearch
'''
es.indices.put_mapping(index=newIndexName, doc_type='weapon_doc', body=weapon_doc_mapping)

print "Created new Index: " + newIndexName + " and assigned mapping for "+ newDocType








#print res