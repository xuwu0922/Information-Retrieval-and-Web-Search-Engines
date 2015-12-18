dedupStringsGen.py:
this code is used to extract essential image information section <url,Parse Metadata,ParseText>
Before using this code, change the value of data_path and text_path inside the dedupStringsGen.py, according to data under the parse_data and parse_text folder

Consider the convenience，every Algorithm's folder has a sample generated file from dedupStringsGen.py, named "stringsForDedup.txt"

After compile the related java file, run: java xxx /path/to/result_file_from_dedupString
eg: $ cd ExacDedupApp
	$ javac ExacDedupApp.java
	$ java ExacDedupApp stringsForDedup.txt

Note: add '-Xlint' for compile if neccessory eg. $ javac -Xlint ExacDedupApp.java