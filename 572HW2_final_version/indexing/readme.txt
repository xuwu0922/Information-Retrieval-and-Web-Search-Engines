****************************************** Run Tika-server, GeoParserTool, cTakes for extraction and indexing ****************************************

First, make sure elasticsearch, tika-server 1.12, and tika python, geo-parser and tika-OCR are all installed.
Also, make sure $TIKA_HOME is defined to point to your tika-trunk home dir. 

Before starting, install tika-python and elasticsearchpy:

	tika-python -->  pip install tika

	elastisearchpy --> pip install elasticsearch

-------------------------------------------------------------------------------------------------------------------------------------------------------

Follow steps below for setting up and indexing:

1. Navigate to home dir of elasticsearch 1.7.3 and start an instance of elastic search:
	bin/elasticsearch

	make sure elasticsearch is running by openning localhost:9200 in browser and seeing basic info of instance of elasticsearch

2. Start 'regular metadata' Tika-server in local port 9998:
	java -jar $TIKA_HOME/tika-server/target/tika-server-1.12-SNAPSHOT.jar

	make sure tika-server is running by openning localhost:9998 in browser and seeing tika-server welcoming message and commands description

3. Start 'geo metadata' Tika-server in local port 9997:
	java -classpath $HOME/src/location-ner-model:$HOME/src/geotopic-mime:$TIKA_HOME/tika-server/target/tika-server-1.12-SNAPSHOT.jar  org.apache.tika.server.TikaServerCli --port=9997

	make sure tika-server is running by openning localhost:9997 in browser and seeing tika-server welcoming message and commands description

4. To run awsEsTikaIndexCreate.py to create 'weapons_tika_index' and create mapping for it
	python awsEsTikaIndexCreate.py
	
5. To index into 'weapons_index_metadata' run awsEsTikaIndexing.py:
	python awsEsTikaIndexing.py <docs dir>

	<docs dir> -> directory where documents to be indexed are stored
	Be mindful that this python script will create the same number of .geot files as there are docs to be indexed in the folder where you are running
	the script

6. To index into 'weapons_index_content' run esMetaBasedIndexing.py:
	run esContentBasedIndexing.py
	python esContentBasedIndexing.py <docs dir>

	<docs dir> -> directory where documents to be indexed are stored


7. To include json data files

	python awsJsonEsIndexCreate.py

	python jsonWeaponEsIndexer.py <json data dir>

	<json data dir> -> directory where provided .json files are located




	