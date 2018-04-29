/**
 * Created by YangLiqiao on 2017/6/16.
 */
$(document).ready(function() {
    var map = L.map('map').setView([27.40, 116.1], 7);
    var noarrival = new L.layerGroup();
    var ctsarrival = new L.layerGroup();
    var centerarrival = new L.layerGroup();
    var directarrival = new L.layerGroup();

    getApi(
        '/cimiss/initregcenter', {
    }, function (err, result) {
        if (err) {
            showError(err);
        } else {
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
    socket.on('reg_center', function(msg){
        var sjson = $.parseJSON(msg);
        info2ponit(sjson);
    });

    function info2ponit(sjson) {
        var ctsArriSum = {'360000':0, '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var centerArriSum = {'360000':0, '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var totalSum = {'360000':0, '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var dt = new Date();
        $('.layertitle')[0].innerHTML = '<h5><strong>区域站 ' + dt.UTCFormat('yyyy-MM-dd HH:00:00') + ' 到报情况</strong></h5>';
        map.removeLayer(noarrival);
        map.removeLayer(ctsarrival);
        map.removeLayer(centerarrival);
        map.removeLayer(directarrival);
        noarrival.clearLayers();
        ctsarrival.clearLayers();
        centerarrival.clearLayers();
        directarrival.clearLayers();
        for (var i=0; i<sjson.length; i++) {
            sno = sjson[i].sno;
            sname = sjson[i].sname;
            acode = sjson[i].areacode;
            lon = parseFloat(sjson[i].lon);
            lat = parseFloat(sjson[i].lat);
            cts = parseInt(sjson[i].cts_arrival);
            center = parseInt(sjson[i].center_arrival);
            var outer_color = "#DB7B3C";
            var inner_color = "#DB7B3C";
            totalSum[acode] = totalSum[acode] + 1;
            totalSum['360000'] = totalSum['360000'] + 1;
            if (cts == 1) {
                outer_color = "green";
                ctsArriSum[acode] = ctsArriSum[acode] + 1;
                ctsArriSum['360000'] = ctsArriSum['360000'] + 1;
            }
            if (center == 1) {
                inner_color = "green";
                centerArriSum[acode] = centerArriSum[acode] + 1;
                centerArriSum['360000'] = centerArriSum['360000'] + 1;
            }
            var markerOptions = {
                radius: 4,
                fillColor: inner_color,
                color: outer_color,
                opacity: 1,
                fillOpacity: 0.8
            };
            if(localStorage.area_code == "360000" || localStorage.area_code == acode) {
                if (cts == 0 && center == 0) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname).addTo(noarrival);
                }else if (cts == 0 && center == 1) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname).addTo(centerarrival);
                } else if (cts == 1 && center == 0) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname).addTo(directarrival);
                } else if (cts == 1 && center == 1) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname).addTo(ctsarrival);
                }
            }
            //if(sjson[i].nocenter == '1') {
            //    $('#center-table-' + key).append('<li>' + sno + '</li>');
            //}
        }
        if($('#noarr')[0].checked) {
            noarrival.addTo(map);
        }
        if($('#ctsarr')[0].checked) {
            ctsarrival.addTo(map);
        }
        if($('#centerarr')[0].checked) {
            centerarrival.addTo(map);
        }
        if($('#directarr')[0].checked) {
            directarrival.addTo(map);
        }

        for (var key in ctsArriSum) {
            if(localStorage.area_code == "360000" || localStorage.area_code ==key) {
                $('#arrival-table-' + key).children('td')[1].innerHTML = totalSum[key];
                $('#arrival-table-' + key).children('td')[2].innerHTML = centerArriSum[key] + '/' + (centerArriSum[key] / totalSum[key] * 100).toFixed(2) + '%';
                $('#arrival-table-' + key).children('td')[3].innerHTML = ctsArriSum[key] + '/' + (ctsArriSum[key] / totalSum[key] * 100).toFixed(2) + '%';
                //$('#arrival-table-' + key).children('td')[2].innerHTML = (arriSum[key] / totalSum[key] * 100).toFixed(2) + '%';
            } else {
                $('#arrival-table-' + key).children('td')[1].innerHTML = '<span class="uk-text-small uk-text-muted" style="font-style:italic">权限不足</span>';
                $('#arrival-table-' + key).children('td')[2].innerHTML = '<span class="uk-text-small uk-text-muted" style="font-style:italic">权限不足</span>';
                $('#arrival-table-' + key).children('td')[3].innerHTML = '<span class="uk-text-small uk-text-muted" style="font-style:italic">权限不足</span>';
            }
        }
    }

    var vm = new Vue({
        el: '#layer-check',
        data: {
            noarr: true,
            ctsarr: true,
            centerarr: true,
            directarr:true
        },
        methods: {
            nocheck: function (event) {
                event.preventDefault();
                map.removeLayer(noarrival);
                if(this.noarr) {
                    noarrival.addTo(map);
                }
            },
            ctscheck: function (event) {
                event.preventDefault();
                map.removeLayer(ctsarrival);
                if(this.ctsarr) {
                    ctsarrival.addTo(map);
                }
            },
            centercheck: function (event) {
                event.preventDefault();
                map.removeLayer(centerarrival);
                if(this.centerarr) {
                    centerarrival.addTo(map);
                }
            },
            directcheck: function (event) {
                event.preventDefault();
                map.removeLayer(directarrival);
                if(this.directarr) {
                    directarrival.addTo(map);
                }
            }
        }
    });
});