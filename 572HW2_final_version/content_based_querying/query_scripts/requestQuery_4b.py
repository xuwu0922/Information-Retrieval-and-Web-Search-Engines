import requests
import json
import sys
reload(sys)
sys.setdefaultencoding("UTF8")
def search(uri, term):
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "size": 0,
        "aggs": {
            "group_by_menu": {
                "terms": {
                    "field": "availableDate"
                },
                "aggs": {
                    "group_by_d": {
                        "terms": {
                            "field": "itemCategory"
                        },
                        "aggs": {
                            "group_by_e": {
                                "terms": {
                                    "field": "location"
                                }
                            }
                        }
                    }
                }
            }
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return results

def format_results(results):
    """Print results nicely:
    doc_id) description
    """
    #print results
    if 'aggregations' in results:
        for e in results["aggregations"]["group_by_menu"]["buckets"]:
            print e["key_as_string"]+", count="+str(e["doc_count"])
            for ee in e["group_by_d"]["buckets"]:
                print ">>>>>"+ee["key"]+", count="+str(ee["doc_count"])
                for eee in ee["group_by_e"]["buckets"]:
                    print eee["key"]+", count="+str(eee["doc_count"])
                print "###################"
            print "*****************************"
    '''if 'hits' in results:
        print("%d documents found:" % results['hits']['total'])
        data = [doc for doc in results['hits']['hits']]
        for doc in data:
            print("doc id: %s " % (doc['_id']))
            print("doc score: %s " % (doc['_score']))
            print("location: %s" % ( doc['_source']['location']))
            print(" description: %s" % ( doc['_source']['description']))
            print(" availableDate: %s" % (doc['_source']['availableDate']))
            print(" sellerDesc: %s" % (doc['_source']['sellerDesc']))
            print(" itemCategory: %s" % (doc['_source']['itemCategory']))
            print(" itemManufacturer: %s" % (doc['_source']['itemManufacturer']))
            
            print(" resourceName: %s" % ( doc['_source']['resourceName']))
            print(" contentType: %s" % ( doc['_source']['contentType']))
            print(" keywords: %s" % ( doc['_source']['keywords']))
            print(" geographicName: %s" % ( doc['_source']['geographicName']))
        else:
            print 'no documents found'''


def create_doc(uri, doc_data={}):
    """Create new document."""
    query = json.dumps(doc_data)
    response = requests.post(uri, data=query)
    print(response)

def main():
    uri_search = 'http://search-csci572-vbd7idisazj5dy44rsanqhhtkq.us-west-2.es.amazonaws.com/json_weapons_index/weapon_doc/_search'

    results = search(uri_search, "gun")
    format_results(results)

    #create_doc(uri_create, {"content": "The fox!"})
    #results = search(uri_search, "fox")
    #format_results(results)

if __name__ == '__main__':
    main()
else:
    print("nblearn loaded as a module")