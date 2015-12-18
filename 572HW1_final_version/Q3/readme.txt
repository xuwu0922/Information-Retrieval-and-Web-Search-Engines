To include the interactive selenium handler in nutch, place the handler java files 
in $NUTCH_HOME/src/plugin/protocol-interactiveselenium/src/java/org/apache/nutch/protocol/interactiveselenium/handlers
and then rebuild nutch. 
The protocol-interactiveselenium protocol needs to be added in nutch_site.xml and the handler name should be added
to the interactiveselenium.handlers property in nutch_site.xml, which is already included in the nutch_site.xml
we submitted.