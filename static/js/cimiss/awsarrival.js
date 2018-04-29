/**
 * Created by YangLiqiao on 2017/6/16.
 */
$(document).ready(function() {
    var map = L.map('map').setView([27.40, 116.1], 7);
    var noarrival = new L.layerGroup();
    var awsarrival = new L.layerGroup();
    var pqcarrival = new L.layerGroup();

    getApi(
        '/cimiss/initaws', {
    }, function (err, result) {
        if (err) {
            showError(err);
        }
        else {
            var sjson = result
            info2ponit(sjson)
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
        var sjson = $.parseJSON(msg)
        info2ponit(sjson)
    });

    socket.on('mytask', function(msg){
        alert("22222");
    });

    $('#test').click(function(event) {
        socket.emit('aws', {data: 1});
        return false;
    });
    $('#task').click(function(event) {
        socket.emit('aws1', {data: 1});
        return false;
    });

    function info2ponit(sjson) {
        var arriSum = {'360000':0, '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var totalSum = {'360000':0, '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var dt = new Date();
        $('.layertitle')[0].innerHTML = '<h5><strong>区域站 ' + dt.UTCFormat('yyyy-MM-dd HH:00:00') + ' 到报情况</strong></h5>';
        map.removeLayer(noarrival);
        map.removeLayer(awsarrival);
        map.removeLayer(pqcarrival);
        noarrival.clearLayers();
        awsarrival.clearLayers();
        pqcarrival.clearLayers();
        for (var i=0; i<sjson.length; i++) {
            sno = sjson[i].sno;
            sname = sjson[i].sname;
            acode = sjson[i].areacode;
            lon = parseFloat(sjson[i].lon);
            lat = parseFloat(sjson[i].lat);
            ori = parseInt(sjson[i].original);
            pqc = parseInt(sjson[i].pqc);
            var outer_color = "#DB7B3C";
            var inner_color = "#DB7B3C";
            totalSum[acode] = totalSum[acode] + 1;
            totalSum['360000'] = totalSum['360000'] + 1;
            if (ori == 1) {
                outer_color = "green";
                arriSum[acode] = arriSum[acode] + 1;
                arriSum['360000'] = arriSum['360000'] + 1;
            }
            if (pqc == 1) {
                inner_color = "green";
            }
            var markerOptions = {
                radius: 4,
                fillColor: inner_color,
                color: outer_color,
                opacity: 1,
                fillOpacity: 0.8
            };
            if(localStorage.area_code == "360000" || localStorage.area_code == acode) {
                if (ori == 0 && pqc == 0) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname).addTo(noarrival);
                } else if (ori == 1 && pqc == 0) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname).addTo(awsarrival);
                } else if (ori == 1 && pqc == 1) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname).addTo(pqcarrival);
                }
            }
            //if(sjson[i].nocenter == '1') {
            //    $('#center-table-' + key).append('<li>' + sno + '</li>');
            //}
        }
        if($('#noarr')[0].checked) {
            noarrival.addTo(map);
        }
        if($('#awsarr')[0].checked) {
            awsarrival.addTo(map);
        }
        if($('#pqcarr')[0].checked) {
            pqcarrival.addTo(map);
        }

        for (var key in arriSum) {
            if(localStorage.area_code == "360000" || localStorage.area_code ==key) {
                $('#arrival-table-' + key).children('td')[1].innerHTML = arriSum[key] + '/' + totalSum[key];
                $('#arrival-table-' + key).children('td')[2].innerHTML = (arriSum[key] / totalSum[key] * 100).toFixed(2) + '%';
            } else {
                $('#arrival-table-' + key).children('td')[1].innerHTML = '<span class="uk-text-small uk-text-muted" style="font-style:italic">权限不足</span>';
                $('#arrival-table-' + key).children('td')[2].innerHTML = '<span class="uk-text-small uk-text-muted" style="font-style:italic">权限不足</span>';
            }
        }
    }

    var vm = new Vue({
        el: '#layer-check',
        data: {
            noarr: true,
            awsarr: true,
            pqcarr: true
        },
        methods: {
            nochenk: function (event) {
                event.preventDefault();
                map.removeLayer(noarrival);
                if(this.noarr) {
                    noarrival.addTo(map);
                }
            },
            awschenk: function (event) {
                event.preventDefault();
                map.removeLayer(awsarrival);
                if(this.awsarr) {
                    awsarrival.addTo(map);
                }
            },
            pqcchenk: function (event) {
                event.preventDefault();
                map.removeLayer(pqcarrival);
                if(this.pqcarr) {
                    pqcarrival.addTo(map);
                }
            }
        }
    });
});