/**
 * Created by YangLiqiao on 2017/6/16.
 */
$(document).ready(function() {
    var map = L.map('map').setView([27.40, 116.1], 7);
    var normal_battery = new L.layerGroup();
    var low_battery = new L.layerGroup();
    var unknown_battery = new L.layerGroup();


    getApi('/cimiss/initawsbattery', {
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
    socket.on('aws_battery', function(msg){
        var sjson = $.parseJSON(msg);
        info2ponit(sjson);
    });


    function info2ponit(sjson) {
        var normalSum = { '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var lowSum = { '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var noSum = { '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var dt = new Date();
        var twoli = '';
        var oneli = '';
        $('.layertitle')[0].innerHTML = '<h5><strong>区域站 ' + dt.UTCFormat('yyyy-MM-dd HH:00:00') + ' 电源状态</strong></h5>';
        map.removeLayer(normal_battery);
        map.removeLayer(low_battery);
        map.removeLayer(unknown_battery);
        normal_battery.clearLayers();
        low_battery.clearLayers();
        unknown_battery.clearLayers();
        $("ul[id^='center-table-']").html("");
        for (var i=0; i<sjson.length; i++) {
            var sno = sjson[i].sno;
            var sname = sjson[i].sname;
            var acode = sjson[i].areacode;
            var lon = parseFloat(sjson[i].lon);
            var lat = parseFloat(sjson[i].lat);
            var machine = sjson[i].machine;
            var county = sjson[i].county;
            var batteryv = parseFloat(sjson[i].battery_value);
            var outer_color = "green";
            var inner_color = "green";
            if (batteryv > 5) {
                normalSum[acode] = normalSum[acode] + 1;
            } else if (batteryv >= 0) {
                outer_color = "#DB7B3C";
                inner_color = "#DB7B3C";
                lowSum[acode] = lowSum[acode] + 1;
            } else if (batteryv == -1.0) {
                outer_color = "#666666";
                inner_color = "#666666";
                noSum[acode] = noSum[acode] + 1;
            }


            var markerOptions = {
                radius: 4,
                fillColor: inner_color,
                color: outer_color,
                opacity: 1,
                fillOpacity: 1
            };

            if(localStorage.area_code == "360000" || localStorage.area_code == acode) {
                if (batteryv >= 5) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname + "<br>设备：" + machine + "<br>县名：" + county + "<br>电压：" + batteryv).addTo(normal_battery);
                } else if(batteryv >= 0) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname + "<br>设备：" + machine + "<br>县名：" + county + "<br>电压：" + batteryv).addTo(low_battery);
                } else if(batteryv == -1.0) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname + "<br>设备：" + machine + "<br>县名：" + county + "<br>电压：" + "缺测").addTo(unknown_battery);
                }
            }

            if(batteryv >= 0 && batteryv < 5) {
                $('#center-table-' + acode).prepend('<li class="uk-text-small"><div class="uk-grid"><div class="uk-width-2-10@m">' + sno + '</div><div class="uk-width-3-10@m">' + machine + '</div><div class="uk-width-3-10@m">' + county + '</div><div class="uk-width-2-10@m">电压'+ batteryv +'</div></div></li>');
            } else if(batteryv == -1.0) {
                $('#center-table-' + acode).append('<li class="uk-text-small"><div class="uk-grid"><div class="uk-width-2-10@m">' + sno + '</div><div class="uk-width-3-10@m">' + machine + '</div><div class="uk-width-3-10@m">' + county + '</div><div class="uk-width-2-10@m">缺测</div></div></li>');
            }
        }
        if($('#normalb')[0].checked) {
            normal_battery.addTo(map);
        }
        if($('#lowb')[0].checked) {
            low_battery.addTo(map);
        }
        if($('#nob')[0].checked) {
            unknown_battery.addTo(map);
        }

        for (var key in lowSum) {
            if(localStorage.area_code == "360000" || localStorage.area_code == key) {
                //$('#tab-' + key).text("(" + nocenterSum[key] + ")");
                $('#center-table-' + key).prepend('<li class="uk-text-small uk-text-bold"><div class="uk-grid"><div class="uk-width-1-3@m">电压不足：' + lowSum[key] + '</div><div class="uk-width-1-3@m">电压缺测：' + noSum[key] + '</div></div></li>');
            }
        }
    }


    var vm = new Vue({
        el: '#layer-check',
        data: {
            normalb: true,
            lowb: true,
            nob: true
        },
        methods: {
            normalcheck: function (event) {
                event.preventDefault();
                map.removeLayer(normal_battery);
                if(this.normalb) {
                    normal_battery.addTo(map);
                }
            },
            lowcheck: function (event) {
                event.preventDefault();
                map.removeLayer(low_battery);
                if(this.lowb) {
                    low_battery.addTo(map);
                }
            },
            unknowncheck: function (event) {
                event.preventDefault();
                map.removeLayer(unknown_battery);
                if(this.nob) {
                    unknown_battery.addTo(map);
                }
            }
        }
    });
});