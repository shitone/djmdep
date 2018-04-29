/**
 * Created by YangLiqiao on 2017/6/16.
 */
$(document).ready(function() {
    var map = L.map('map').setView([27.40, 116.1], 7);
    var centersource = new L.layerGroup();
    var citysource = new L.layerGroup();
    var unknownsource = new L.layerGroup();
    var intersource = new L.layerGroup();


    getApi('/cimiss/initawssource', {
    }, function (err, result) {
        if (err) {
            showError(err);
        }
        else {
            var sjson = result;
            info2ponit(sjson);
        }
    });

    L.tileLayer('http://10.116.32.88/mapserver.php?t=t&x={x}&y={y}&z={z}', {
            attribution: '&copy; <a>江西省气象信息中心</a> contributors'
    }).addTo(map);


    new L.WFS({
        url: 'http://10.116.32.244:8080/geoserver/jiangxi/ows',
        typeNS: 'jiangxi',
        typeName: 'jx_outer',
        crs: L.CRS.EPSG4326,
        geometryField: 'the_geom',
        style: {
          color: 'black',
          weight: 0.5
        }
    }).addTo(map);

    new L.WFS({
        url: 'http://10.116.32.244:8080/geoserver/jiangxi/ows',
        typeNS: 'jiangxi',
        typeName: 'jx_all',
        crs: L.CRS.EPSG4326,
        geometryField: 'the_geom',
        style: {
          color: 'black',
          weight: 0.5
        }
    }).addTo(map);


    var socket = io.connect('http://' + document.domain + ':' + location.port + '/awspqc');
    socket.on('aws_info', function(msg){
        var sjson = $.parseJSON(msg);
        info2ponit(sjson);
    });


    function info2ponit(sjson) {
        var centerSum = { '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var nocenterSum = { '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var intercenterSum = { '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var dt = new Date();
        var twoli = '';
        var oneli = '';
        $('.layertitle')[0].innerHTML = '<h5><strong>区域站 ' + dt.UTCFormat('yyyy-MM-dd HH:00:00') + ' 来源分析</strong></h5>';
        map.removeLayer(centersource);
        map.removeLayer(citysource);
        map.removeLayer(unknownsource);
        map.removeLayer(intersource);
        centersource.clearLayers();
        citysource.clearLayers();
        unknownsource.clearLayers();
        intersource.clearLayers();
        $("ul[id^='center-table-']").html("");
        for (var i=0; i<sjson.length; i++) {
            var sno = sjson[i].sno;
            var sname = sjson[i].sname;
            var acode = sjson[i].areacode;
            var lon = parseFloat(sjson[i].lon);
            var lat = parseFloat(sjson[i].lat);
            var machine = sjson[i].machine;
            var county = sjson[i].county;
            var nocenter = parseInt(sjson[i].nocenter);
            var outer_color = "green";
            var inner_color = "green";
            if (nocenter == 0) {
                centerSum[acode] = centerSum[acode] + 1;
            }
            if (nocenter == 1) {
                outer_color = "#DB7B3C";
                inner_color = "#DB7B3C";
                nocenterSum[acode] = nocenterSum[acode] + 1;
            }
            if (nocenter == 3) {
                outer_color = "red";
                inner_color = "red";
                intercenterSum[acode] = intercenterSum[acode] + 1;
            }
            if (nocenter == 2) {
                outer_color = "#666666";
                inner_color = "#666666";
            }


            var markerOptions = {
                radius: 4,
                fillColor: inner_color,
                color: outer_color,
                opacity: 1,
                fillOpacity: 1
            };

            if(localStorage.area_code == "360000" || localStorage.area_code == acode) {
                if (nocenter == 1) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname + "<br>设备：" + machine + "<br>县名：" + county).addTo(citysource);
                } else if(nocenter == 2) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname + "<br>设备：" + machine + "<br>县名：" + county).addTo(unknownsource);
                } else if(nocenter == 3) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname + "<br>设备：" + machine + "<br>县名：" + county).addTo(intersource);
                } else {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname + "<br>设备：" + machine + "<br>县名：" + county).addTo(centersource);
                }
            }

            if(sjson[i].nocenter == '1') {
                $('#center-table-' + acode).append('<li class="uk-text-small"><div class="uk-grid"><div class="uk-width-2-10@m">' + sno + '</div><div class="uk-width-3-10@m">' + machine + '</div><div class="uk-width-3-10@m">' + county + '</div><div class="uk-width-2-10@m">地市</div></div></li>');
            }

            if(sjson[i].nocenter == '3') {
                $('#center-table-' + acode).prepend('<li class="uk-text-small"><div class="uk-grid"><div class="uk-width-2-10@m">' + sno + '</div><div class="uk-width-3-10@m">' + machine + '</div><div class="uk-width-3-10@m">' + county + '</div><div class="uk-width-2-10@m">并传</div></div></li>');
            }
        }
        if($('#centerst')[0].checked) {
            centersource.addTo(map);
        }
        if($('#cityst')[0].checked) {
            citysource.addTo(map);
        }
        if($('#unknownst')[0].checked) {
            unknownsource.addTo(map);
        }
        if($('#interst')[0].checked) {
            intersource.addTo(map);
        }

        for (var key in nocenterSum) {
            if(localStorage.area_code == "360000" || localStorage.area_code == key) {
                //$('#tab-' + key).text("(" + nocenterSum[key] + ")");
                $('#center-table-' + key).prepend('<li class="uk-text-small uk-text-bold"><div class="uk-grid"><div class="uk-width-1-3@m">仅省级：' + centerSum[key] + '</div><div class="uk-width-1-3@m">并传：' + intercenterSum[key] + '</div><div class="uk-width-1-3@m">仅市级：'+nocenterSum[key]+'</div></div></li>');
            }
        }
    }


    var vm = new Vue({
        el: '#layer-check',
        data: {
            centerst: true,
            cityst: true,
            unknownst: true,
            interst: true
        },
        methods: {
            centercheck: function (event) {
                event.preventDefault();
                map.removeLayer(centersource);
                if(this.centerst) {
                    centersource.addTo(map);
                }
            },
            citycheck: function (event) {
                event.preventDefault();
                map.removeLayer(citysource);
                if(this.cityst) {
                    citysource.addTo(map);
                }
            },
            unknowncheck: function (event) {
                event.preventDefault();
                map.removeLayer(unknownsource);
                if(this.unknownst) {
                    unknownsource.addTo(map);
                }
            },
            intercheck: function (event) {
                event.preventDefault();
                map.removeLayer(intersource);
                if(this.interst) {
                    intersource.addTo(map);
                }
            }
        }
    });
});