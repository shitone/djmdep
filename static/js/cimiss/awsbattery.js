/**
 * Created by YangLiqiao on 2017/6/16.
 */
$(document).ready(function() {
    var map = L.map('map', {contextmenu: true, contextmenuWidth: 100,}).setView([27.40, 116.1], 7);
    var normal_battery = new L.layerGroup();
    var low_battery = new L.layerGroup();
    var unknown_battery = new L.layerGroup();

    var htable = $("#awsbattery_table").DataTable({
        "order": [],
        language: {
            "sProcessing": "处理中...",
            "sLengthMenu": "每页 _MENU_ 项",
            "sZeroRecords": "没有匹配结果",
            "sInfo": "共_TOTAL_项",
            "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
            "sInfoFiltered": "",
            "sInfoPostFix": "",
            "sSearch": "搜索:",
            "sUrl": "",
            "sEmptyTable": "无记录",
            "sLoadingRecords": "载入中...",
            "sInfoThousands": ",",
            "oPaginate": {
                "sFirst": "<<",
                "sPrevious": "<",
                "sNext": ">",
                "sLast": ">>"
            },
            "oAria": {
                "sSortAscending": ": 以升序排列此列",
                "sSortDescending": ": 以降序排列此列"
            }
        },
        "iDisplayLength": 15,
        "deferRender": true,
        "sScrollY" : 510,
        "dom": '<"row"<"col-md-4" i><"col-md-8" f>>rt<"d-flex justify-content-center"p><"clear">',
        // "aoColumnDefs": [ { "bSortable": false, "aTargets": [ ] }]
    });


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


    const webSocketBridge = new channels.WebSocketBridge();
    webSocketBridge.connect('/ws/cimiss/awspqc/awsbattery');
    webSocketBridge.listen(function(action, stream) {
        var sjson = $.parseJSON(action.message);
        htable.clear();
        info2ponit(sjson);
    });


    // function set_threshold (e) {
    //     // $('#exampleModal').modal('show');
    //     map.panTo(e.latlng);
    // }

    $('#exampleModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var sno = button.data('sno');
        var thre = button.data('thre');
        var modal = $(this);
        modal.find('#exampleModalLabel').text(sno);
        modal.find('.modal-body input').val(thre);
    });


    $('#sethre').click(function(){
        var sno = $('#exampleModalLabel').text();
        var thre = $('#recipient-name').val();
        postApi('/cimiss/batterythreshold/' + sno + '/' + thre , {
        }, function (err, result) {
            $('#exampleModal').modal('hide');
            if (err) {
                showError(err);
            }
            else {
                if (result.succeed) {
                    alert('修改成功')
                } else {
                    alert('修改失败')
                }
            }
        });
    });


    function info2ponit(sjson) {
        var code2city = { '360100':'南昌','360200':'景德镇','360300':'萍乡','360400':'九江','360500':'新余',
            '360600':'鹰潭','360700':'赣州','360800':'吉安','360900':'宜春','361000':'抚州', '361100':'上饶'};
        var normalSum = { '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var lowSum = { '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var noSum = { '360100':0,'360200':0,'360300':0,'360400':0,'360500':0,'360600':0,'360700':0,'360800':0,'360900':0,'361000':0, '361100':0};
        var dt = new Date();
        var twoli = '';
        var oneli = '';
        $('.layertitle')[0].innerHTML = '<h6 class="m-0"><strong>区域站 ' + dt.UTCFormat('yyyy-MM-dd HH:00:00') + ' 电源状态</strong></h6>';
        map.removeLayer(normal_battery);
        map.removeLayer(low_battery);
        map.removeLayer(unknown_battery);
        normal_battery.clearLayers();
        low_battery.clearLayers();
        unknown_battery.clearLayers();
        $("ul[id^='center-table-']").html("");
        var source_dataset = [];
        for (var i=0; i<sjson.length; i++) {
            var sno = sjson[i].sno;
            var sname = sjson[i].sname;
            var acode = sjson[i].areacode;
            var lon = parseFloat(sjson[i].lon);
            var lat = parseFloat(sjson[i].lat);
            var machine = sjson[i].machine;
            var county = sjson[i].county;
            var batteryv = parseFloat(sjson[i].battery_value);
            var thresholds = parseFloat(sjson[i].thresholds);
            var outer_color = "green";
            var inner_color = "green";
            if (batteryv > thresholds) {
                normalSum[acode] = normalSum[acode] + 1;
            } else if (batteryv >= 0) {
                outer_color = "#DB7B3C";
                inner_color = "#DB7B3C";
                lowSum[acode] = lowSum[acode] + 1;
            } else if ((batteryv == -1.0) || isNaN(batteryv)) {
                outer_color = "#666666";
                inner_color = "#666666";
                noSum[acode] = noSum[acode] + 1;
            }


            var markerOptions = {
                radius: 4,
                fillColor: inner_color,
                color: outer_color,
                opacity: 1,
                fillOpacity: 1,
                // contextmenu: true,
                // contextmenuInheritItems: false,
                // contextmenuItems: [
                //     {
                //         text: '<div class="abc" value="' + sno +'">设置电量阈值</div>',
                //         // callback:set_threshold
                //     }
                // ]
            };

            if(localStorage.area_code == "360000" || localStorage.area_code == acode) {
                if (batteryv >= thresholds) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname + "<br>设备：" + machine + "<br>县名：" + county + "<br>电压：" + batteryv+ "<br>阈值：" + thresholds
                        + "&nbsp<button type='button' data-toggle='modal' data-target='#exampleModal' data-sno='" + sno + "' data-thre='" + thresholds + "'>设置</button>").addTo(normal_battery);
                } else if(batteryv >= 0) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname + "<br>设备：" + machine + "<br>县名：" + county + "<br>电压：" + batteryv+ "<br>阈值：" + thresholds
                        + "&nbsp<button type='button' data-toggle='modal' data-target='#exampleModal' data-sno='" + sno + "' data-thre='" + thresholds + "'>设置</button>").addTo(low_battery);
                } else if(batteryv == -1.0) {
                    L.circleMarker([lat, lon], markerOptions).bindPopup("站号：" + sno + "<br>站名：" + sname + "<br>设备：" + machine + "<br>县名：" + county + "<br>电压：" + "缺测"+ "<br>阈值：" + thresholds
                        + "&nbsp<button type='button' data-toggle='modal' data-target='#exampleModal' data-sno='" + sno + "' data-thre='" + thresholds + "'>设置</button>").addTo(unknown_battery);
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

            var source_row = [sno,code2city[acode],county,machine];

            if(batteryv >= 0 && batteryv < thresholds) {
                source_row = [sno,code2city[acode],county,machine,batteryv];
                source_dataset.push(source_row);
            } else if(batteryv == -1.0) {
                source_row = [sno,code2city[acode],county,machine,'缺测'];
                source_dataset.push(source_row);
            }
        }
        htable.rows.add(source_dataset).draw();


        // for (var key in lowSum) {
        //     if(localStorage.area_code == "360000" || localStorage.area_code == key) {
        //         //$('#tab-' + key).text("(" + nocenterSum[key] + ")");
        //         $('#center-table-' + key).prepend('<li class="uk-text-small uk-text-bold"><div class="uk-grid"><div class="uk-width-1-3@m">电压不足：' + lowSum[key] + '</div><div class="uk-width-1-3@m">电压缺测：' + noSum[key] + '</div></div></li>');
        //     }
        // }
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