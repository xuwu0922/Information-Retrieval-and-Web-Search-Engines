This is link based algorithm code, used to construct node, graph and then linking and scoring

First, if you need to import networkx (we just use it like a list/set to store all nodes inside it effectively, we don't use it to do other graph related operations, like add_edges...)

command:

$pip install networkx

$python link_based_ranker.py /path/to/json_files_collection_folder/ '["keywords1","keywords",...]' "field1" "field2"...

sample(use sample_json_collection in the same folder): 

	for query 4-a: $python link_based_ranker.py sample_json_collection/ '["grenade","rocket","explosive"]' "description"

if no keywords provided, the keywords list still need to be argument with empty vaule

	for query 4-b: $python link_based_ranker.py sample_json_collection/ '[]' "availableDate" "itemCategory" "location"

The scored query result "sorted.txt" will be generate after executing the code, showing 20 top scored files 

The following are the commands we use to run our link based algorithm to answer questions:


4.a: python link_based_ranker.py set/ '["looking to buy"]' "location" "description" "availableDate"

4.b: python link_based_ranker.py set/ '[]' "availableDate" "itemCategory" "location"

4.c: python link_based_ranker.py set/ '[]' "availableDate" "itemManufacturer"

4.d: python link_based_ranker.py set/ '["serial number", "no", "not"]' "description"

4.e: python linkbased_jerry_sort.py set/ '["grenade","rocket","explosive"]' "description"


NOTE: we ran query scripts with entire set of json data, i.e. /set contains entire json data set