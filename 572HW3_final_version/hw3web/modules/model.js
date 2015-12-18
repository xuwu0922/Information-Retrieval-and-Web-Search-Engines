/**
 * Created by Joey on 11/17/15.
 */
var queryBodyA = {
    size: 0,
    query: {
        simple_query_string: {
            query: "looking to buy",
            fields: ["description"],
            default_operator: "and"
        }
    },
    aggs: {
        group_by_date: {
            terms: {
                field: "availableDate"
            },
            aggs: {
                group_by_area: {
                    terms: {
                        field: "location"
                    }
                }
            }
        }
    }
};

var queryBodyB = {
    size: 0,
    aggs: {
        group_by_menu: {
            terms: {
                field: "availableDate"
            },
            aggs: {
                group_by_d: {
                    terms: {
                        field: "itemCategory"
                    },
                    aggs: {
                        group_by_e: {
                            terms: {
                                field: "location"
                            }
                        }

                    }
                }
            }
        }
    }
}

var queryBodyC = {
    size: 0,
    aggs: {
        group_by_menu: {
            terms: {
                field: "availableDate"
            },
            aggs: {
                group_by_d: {
                    terms: {
                        field: "itemManufacturer"
                    }
                }
            }
        }
    }
}

var queryBodyD = {
    "from": 0, "size": 10,
    "query": {
        "bool": {
            "must": {
                "match": {
                    "description": {
                        "query": "serial number",
                        "boost": 3
                    }
                }
            },
            "should": {
                "match": {
                    "description": {
                        "query": "nor",
                        "boost": 2.5
                    }
                }
            },
            "should": {
                "match": {
                    "description": {
                        "query": "no",
                        "boost": 2
                    }
                }
            },
            "should": {
                "match": {
                    "description": {
                        "query": "not",
                        "boost": 1.7
                    }
                }
            }
        }
    }
}
var queryBodyOther = {
    "from" : 0, "size" : 500,
    "query": {
        "bool": {
            "must": {
                "match": {
                    "description": {
                        "query": "serial number",
                        "boost":2
                    }
                }
            },
            "should": {
                "match": {
                    "description": {
                        "query": "no",
                        "boost":1.2
                    }
                }
            },
            "should": {
                "match": {
                    "description": {
                        "query": "not",
                        "boost":1.2
                    }
                }
            }
        }
    }
}


var listA = [];
var listB = [];
var listC = [];
var listD = [];
var listOther = [];
var listOther2 = [
    {
        "key": "Number of posts",
        "color": "#1f77b4",
        "values": []
    }
];