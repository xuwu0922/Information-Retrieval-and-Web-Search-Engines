angular.module('maintenance')
    .factory('queryapi', queryapi)
    .controller('queryCtrl', QueryCtrl)
    .constant('apiUrl',
        'http://search-csci572-vbd7idisazj5dy44rsanqhhtkq.us-west-2.es.amazonaws.com/json_weapons_index_2/weapon_doc/_search');

function queryapi($http, apiUrl) {

    function get(param) {
        return request("GET", param);
    }

    function post(data) {
        return request("POST", null, data);
    }

    function put(data) {
        return request("PUT", null, data);
    }

    function del(param) {
        return request("DELETE", param);
    }

    function request(verb, param, data) {
        var req = {
            method: verb,
            url: url(param),
            data: data
        }
        return $http(req);
    }

    function url(param) {
        if (param == null || !angular.isDefined(param)) {
            param = '';
        }
        return apiUrl + param;
    }

    return {
        getQuery: function (queryBody) {
            return post(queryBody)
        }
    }
}

function QueryCtrl($scope, queryapi) {
    var isBusy = false;

    $scope.isLoading = isLoading;
    $scope.errorMessage = '';
    $scope.hasError = hasError;
    $scope.session = '';
    $scope.queryA = queryA;
    $scope.queryB = queryB;
    $scope.queryC = queryC;
    $scope.queryD = queryD;
    $scope.queryE = queryE;
    $scope.queryOther = queryOther;
    $scope.queryOther2 = queryOther2;
    $scope.listA = listA;
    $scope.listB = listB;
    $scope.listC = listC;
    $scope.listD = listD;


    reset();

    function isLoading() {
        return isBusy == true;
    }

    function reset() {
        isBusy = false;
        $scope.session = '';
    }

    function queryA() {
        if (listA.length != 0)listA = [];
        isBusy = true;
        $scope.session = 'queryA';
        queryapi.getQuery(queryBodyA)
            .success(function (data) {
                isBusy = false;
                $scope.errorMessage = '';
                if (data.aggregations != null && data.aggregations != undefined) {
                    var timeList = [];
                    for (var i = 0; i < data.aggregations.group_by_date.buckets.length; i++) {//
                        var dateObj = data.aggregations.group_by_date.buckets[i];
                        if (dateObj.key < 0) continue;
                        if (!(dateObj.key in timeList)) {
                            timeList.push(dateObj.key);
                        }
                        for (var j = 0; j < dateObj.group_by_area.buckets.length; j++) {
                            var areaObj = dateObj.group_by_area.buckets[j];
                            var flag = false;
                            var k = 0;
                            for (k = 0; k < listA.length; k++) {
                                if (listA[k].key === areaObj.key) {
                                    flag = true;
                                    break;
                                }
                            }
                            if (flag) listA[k].values.push([dateObj.key, areaObj.doc_count]);
                            else {
                                var newObj = {
                                    key: areaObj.key,
                                    values: [[dateObj.key, areaObj.doc_count]]
                                }
                                listA.push(newObj);
                            }
                        }
                    }
                    //alert(timeList.length);
                    //alert(timeList);
                    for (var i = 0; i < listA.length; i++) {
                        for (var j = 0; j < timeList.length; j++) {
                            var exist = false;
                            //alert("listA[i].values.length = "+listA[i].values.length);
                            for (var k = 0; k < listA[i].values.length; k++) {
                                //alert("timeList="+timeList[j]+", listA[i]="+listA[i].values[k]);
                                //alert("listA[i].values[k][0]="+listA[i].values[k][0]);
                                if (timeList[j] == listA[i].values[k][0]) {
                                    //alert("dup!!!");
                                    exist = true;
                                    break;
                                }
                            }
                            //alert("exist="+exist);
                            if (!exist) {
                                listA[i].values.push([timeList[j], 0]);
                            }
                        }
                        listA[i].values.sort();
                    }
                    chartA();
                } else {
                    $scope.errorMessage = 'No data (aggregations) found!';
                }
            })
            .error(
                function (errorInfo, status) {
                    setError(errorInfo, status, -2)
                });


    }

    function queryB() {
        if (listB.length != 0)listB = [];
        isBusy = true;
        $scope.session = 'queryB';
        queryapi.getQuery(queryBodyB)
            .success(function (data) {
                isBusy = false;
                $scope.errorMessage = '';
                if (data.aggregations != null && data.aggregations != undefined) {
                    var timeList = [];
                    for (var i = 0; i < data.aggregations.group_by_menu.buckets.length; i++) {//
                        var dateObj = data.aggregations.group_by_menu.buckets[i];
                        if (dateObj.key < 0) continue;
                        if (!(dateObj.key in timeList)) {
                            timeList.push(dateObj.key);
                        }
                        for (var j = 0; j < dateObj.group_by_d.buckets.length; j++) {
                            var areaObj = dateObj.group_by_d.buckets[j];
                            var groupLabel = areaObj.key;
                            if(groupLabel=="" || (groupLabel==null || groupLabel == undefined)){
                                groupLabel = "N/A";
                            }
                            //alert(areaObj.key)
                            var flag = false;
                            var k = 0;
                            for (k = 0; k < listB.length; k++) {
                                if (listB[k].key === groupLabel) {
                                    flag = true;
                                    break;
                                }
                            }
                            if (flag) listB[k].values.push([dateObj.key, areaObj.doc_count]);
                            else {
                                var newObj = {
                                    key: groupLabel,
                                    values: [[dateObj.key, areaObj.doc_count]]
                                }
                                listB.push(newObj);
                            }
                        }
                    }
                    //alert(timeList.length);
                    //alert(timeList);
                    for (var i = 0; i < listB.length; i++) {
                        for (var j = 0; j < timeList.length; j++) {
                            var exist = false;
                            //alert("listA[i].values.length = "+listA[i].values.length);
                            for (var k = 0; k < listB[i].values.length; k++) {
                                //alert("timeList="+timeList[j]+", listA[i]="+listA[i].values[k]);
                                //alert("listA[i].values[k][0]="+listA[i].values[k][0]);
                                if (timeList[j] == listB[i].values[k][0]) {
                                    //alert("dup!!!");
                                    exist = true;
                                    break;
                                }
                            }
                            //alert("exist="+exist);
                            if (!exist) {
                                listB[i].values.push([timeList[j], 0]);
                            }
                        }
                        listB[i].values.sort();

                    }
                    chartB();
                } else {
                    $scope.errorMessage = 'No data (aggregations) found!';
                }
            })
            .error(
                function (errorInfo, status) {
                    setError(errorInfo, status, -2)
                });
    }

    function queryC() {
        if (listC.length != 0)listC = [];
        isBusy = true;
        $scope.session = 'queryC';
        queryapi.getQuery(queryBodyC)
            .success(function (data) {
                isBusy = false;
                $scope.errorMessage = '';
                if (data.aggregations != null && data.aggregations != undefined) {
                    var timeList = [];
                    for (var i = 0; i < data.aggregations.group_by_menu.buckets.length; i++) {//
                        var dateObj = data.aggregations.group_by_menu.buckets[i];
                        if (dateObj.key < 0) continue;
                        if (!(dateObj.key in timeList)) {
                            timeList.push(dateObj.key);
                        }
                        for (var j = 0; j < dateObj.group_by_d.buckets.length; j++) {
                            var areaObj = dateObj.group_by_d.buckets[j];
                            //alert(areaObj.key)
                            var flag = false;
                            var k = 0;
                            for (k = 0; k < listC.length; k++) {
                                if (listC[k].key === areaObj.key) {
                                    flag = true;
                                    break;
                                }
                            }
                            if (flag) listC[k].values.push([dateObj.key, areaObj.doc_count]);
                            else {
                                var newObj = {
                                    key: areaObj.key,
                                    values: [[dateObj.key, areaObj.doc_count]]
                                }
                                listC.push(newObj);
                            }
                        }
                    }
                    //alert(timeList.length);
                    //alert(timeList);
                    for (var i = 0; i < listC.length; i++) {
                        for (var j = 0; j < timeList.length; j++) {
                            var exist = false;
                            //alert("listA[i].values.length = "+listA[i].values.length);
                            for (var k = 0; k < listC[i].values.length; k++) {
                                //alert("timeList="+timeList[j]+", listA[i]="+listA[i].values[k]);
                                //alert("listA[i].values[k][0]="+listA[i].values[k][0]);
                                if (timeList[j] == listC[i].values[k][0]) {
                                    //alert("dup!!!");
                                    exist = true;
                                    break;
                                }
                            }
                            //alert("exist="+exist);
                            if (!exist) {
                                listC[i].values.push([timeList[j], 0]);
                            }
                        }
                        listC[i].values.sort();

                    }
                    listC[0].bar = true;
                    chartC();
                } else {
                    $scope.errorMessage = 'No data (aggregations) found!';
                }
            })
            .error(
                function (errorInfo, status) {
                    setError(errorInfo, status, -2)
                });
    }

    function queryD() {
        if (listD.length != 0)listD = [];
        isBusy = true;
        $scope.session = 'queryD';
        queryapi.getQuery(queryBodyD)
            .success(function (data) {
                isBusy = false;
                $scope.errorMessage = '';
                if (data.hits != null && data.hits != undefined) {
                    for (var i = 0; i < data.hits.hits.length; i++) {//
                        var obj = data.hits.hits[i];
                        //alert(obj._source.description);
                        var newObj = {
                            //title: obj._source.title,
                            label: obj._source.description,
                            value: obj._score * 100
                        }
                        listD.push(newObj);
                    }
                    chartD();
                } else {
                    $scope.errorMessage = 'No data (hits) found!';
                }
            })
            .error(
                function (errorInfo, status) {
                    setError(errorInfo, status, -2)
                });


    }

    function queryE() {
        $scope.session = 'queryE';
        //alert("session=" + $scope.session);
    }

    function queryOther() {
        if (listOther.length != 0)listOther = [];
        isBusy = true;
        $scope.session = 'queryOther';
        queryapi.getQuery(queryBodyOther)
            .success(function (data) {
                isBusy = false;
                $scope.errorMessage = '';
                if (data.hits.hits.length!=0) {
                    for (var i = 0; i < data.hits.hits.length; i++) {
                        var dateObj = data.hits.hits[i];
                        var groupLabel = dateObj._source.itemCategory;
                        if((groupLabel == null || groupLabel == undefined) ||  groupLabel==""){
                            groupLabel="None";
                        }

                        var keyIndex = -1;
                        for(var k= 0; k<listOther.length;k++){
                            if(listOther[k].key===groupLabel){
                                keyIndex = k;
                                break;
                            }
                        }
                        var score = dateObj._score;
                        var price = dateObj._source.price;
                        if((score == null || score == undefined) ||  score==""){
                            score="0";
                        }
                        if((price == null || price == undefined) ||  (isNaN(price) || price=="")){
                            price="100";
                        }
                        if(keyIndex<0){
                            listOther.push({
                                key: groupLabel,
                                values: []
                            });
                            listOther[listOther.length-1].values.push({
                                x: score,
                                y: price,
                                size: price
                            });
                        }else{
                            listOther[keyIndex].values.push({
                                x: score,
                                y: price,
                                size: price
                            });
                        }
                    }
                    /*var random = d3.random.normal();
                    for (i = 0; i < 4; i++) {
                        listOther.push({
                            key: 'Group ' + i,
                            values: []
                        });

                        for (j = 0; j < 30; j++) {
                            listOther[i].values.push({
                                x: random()
                                , y: random()
                                , size: Math.random()
                            });
                        }
                    }*/
                    otherChart();
                } else {
                    $scope.errorMessage = 'No data (aggregations) found!';
                }
            })
            .error(
                function (errorInfo, status) {
                    setError(errorInfo, status, -2)
                });
    }

    function queryOther2() {
        if (listOther2.length != 0){
            listOther2 = [
                {
                    "key": "Number of posts",
                    "color": "#1f77b4",
                    "values": []
                }
            ];
        }
        isBusy = true;
        $scope.session = 'queryOther';
        queryapi.getQuery(queryBodyOther)
            .success(function (data) {
                isBusy = false;
                $scope.errorMessage = '';
                if (data.hits.hits.length!=0) {
                    for (var i = 0; i < data.hits.hits.length; i++) {
                        var dateObj = data.hits.hits[i]._source;
                        var menuf = dateObj.itemManufacturer;
                        if((menuf==null || menuf==undefined) || menuf==""){
                            menuf="N/A"
                        }
                        var isExisted = -1;
                        for(var j=0;j<listOther2[0].values.length;j++){
                            if(listOther2[0].values[j].label==menuf){
                                isExisted = j;
                                listOther2[0].values[j].value++;
                                break
                            }
                        }
                        if(isExisted<0){
                            listOther2[0].values.push({
                                "label" : menuf ,
                                "value" : 1
                            });
                        }
                    }
                } else {
                    $scope.errorMessage = 'No data (aggregations) found!';
                }
                otherChart2();
            })
            .error(
                function (errorInfo, status) {
                    setError(errorInfo, status, -2)
                });
    }


    function chartA() {
        nv.addGraph(function () {
            var chart = nv.models.stackedAreaChart()
                .x(function (d) {
                    return d[0]
                })
                .y(function (d) {
                    return d[1]
                })
                .clipEdge(true)
                .useInteractiveGuideline(true)
                ;

            chart.xAxis
                .showMaxMin(false)
                .tickFormat(function (d) {
                    return d3.time.format('%x')(new Date(d))
                });

            chart.yAxis
                .tickFormat(d3.format(',.2f'));

            d3.select('#chartA svg')
                .datum(listA)
                .transition().duration(500).call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        });
    }

    function chartB() {
        nv.addGraph(function () {
            var chart = nv.models.cumulativeLineChart()
                .x(function (d) {
                    return d[0]
                })
                //adjusting, 100% is 1.00, not 100 as it is in the data
                .y(function (d) {
                    return d[1] / 100
                })
                .color(d3.scale.category10().range())
                .useInteractiveGuideline(true)
                ;

            chart.xAxis
                .tickFormat(function (d) {
                    return d3.time.format('%x')(new Date(d))
                });

            chart.yAxis.tickFormat(d3.format(',.1%'));

            d3.select('#chartB svg')
                .datum(listB)
                .transition().duration(500)
                .call(chart)
            ;

            nv.utils.windowResize(chart.update);

            return chart;
        });

    }

    function chartC() {
        nv.addGraph(function () {
            var chart = nv.models.linePlusBarChart()
                .margin({top: 30, right: 60, bottom: 50, left: 70})
                .x(function (d, i) {
                    return i
                })
                .y(function (d) {
                    return d[1]
                })
                .color(d3.scale.category10().range())
                ;

            chart.xAxis
                .showMaxMin(false)
                .tickFormat(function (d) {
                    var dx = listC[0].values[d] && listC[0].values[d][0] || 0;
                    return d3.time.format('%x')(new Date(dx))
                });

            chart.y1Axis
                .tickFormat(d3.format(',f'));

            chart.y2Axis
                .tickFormat(function (d) {
                    return d3.format(',f')(d)
                });

            chart.bars.forceY([0]);

            d3.select('#chartC svg')
                .datum(listC)
                .transition().duration(500)
                .call(chart)
            ;

            nv.utils.windowResize(chart.update);

            return chart;
        });
    }

    function chartD() {
        nv.addGraph(function () {
            var chart = nv.models.pieChart()
                .x(function (d) {
                    return d.label
                })
                .y(function (d) {
                    return d.value
                })
                .showLabels(true)     //Display pie labels
                .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
                .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
                .donut(true)          //Turn on Donut mode. Makes pie chart look tasty!
                .donutRatio(0.35)     //Configure how big you want the donut hole size to be.
                ;

            d3.select("#chartD svg")
                .datum(listD)
                .transition().duration(350)
                .call(chart);

            return chart;
        });
    }

    function otherChart() {
        nv.addGraph(function() {
            var chart = nv.models.scatterChart()
                .showDistX(true)
                .showDistY(true)
                .color(d3.scale.category10().range());

            chart.xAxis.tickFormat(d3.format('.02f'));
            chart.yAxis.tickFormat(d3.format('.02f'));

            d3.select('#chartOther svg')
                .datum(listOther)
                .transition().duration(500)
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        });
    }

    function otherChart2() {
        nv.addGraph(function() {
            var chart = nv.models.multiBarHorizontalChart()
                .x(function(d) { return d.label })
                .y(function(d) { return d.value })
                .margin({top: 30, right: 20, bottom: 50, left: 175})
                .showValues(true)
                //.tooltips(false)
                .showControls(false);

            chart.yAxis
                .tickFormat(d3.format(',.2f'));

            d3.select('#chartOther2 svg')
                .datum(listOther2)
                .transition().duration(500)
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        });
    }

    function hasError() {
        return $scope.errorMessage != '';
    }

    function setError(errorInfo, status, id) {
        reset();
        if (status == 401) {
            $scope.errorMessage = "Authorization failed."
        } else {
            $scope.errorMessage = errorInfo.message;
        }
    }
}