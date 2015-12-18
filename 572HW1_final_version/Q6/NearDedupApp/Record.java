// Created by Xu Wu

// class Record {
//     public String url = null;
//     public String parseText = null;

//     public Record(String _url, String _parseText) {
//         url = _url;
//         parseText = _parseText;
//     }
// }


public class Record{
    public String url = null;
    public String metadata = null;
    public String parseText = null;

    public Record(String _url, String _parseMetaData, String _parseText) {
        url = _url;
        metadata = _parseMetaData;
        parseText = _parseText;
    }
}