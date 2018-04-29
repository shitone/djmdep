$(document).ready(function() {
    var daystr = moment.utc().format('YYYY-MM-DD');
    var fp = $("#awsdate").flatpickr();
    var htable = $("#history_table").DataTable({
        "order": [],
        language: {
            "sProcessing": "处理中...",
            "sLengthMenu": "每页 _MENU_ 项",
            "sZeroRecords": "没有匹配结果",
            "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
            "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
            "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
            "sInfoPostFix": "",
            "sSearch": "搜索:",
            "sUrl": "",
            "sEmptyTable": "无记录",
            "sLoadingRecords": "载入中...",
            "sInfoThousands": ",",
            "oPaginate": {
                "sFirst": "首页",
                "sPrevious": "上页",
                "sNext": "下页",
                "sLast": "末页"
            },
            "oAria": {
                "sSortAscending": ": 以升序排列此列",
                "sSortDescending": ": 以降序排列此列"
            }
        },
        "deferRender": true,
        "aoColumnDefs": [ { "bSortable": false, "aTargets": [5, 6, 7, 8, 9 ] }]
    });

    initPage();
    function initPage() {
        fp.setDate(daystr);
        getApi(
            '/cimiss/getawshistory/'+daystr, {
        }, function (err, sjson) {
            if (err) {
                showError(err);
            } else {
                data2table(sjson)
            }
        });
    }

    var vm = new Vue({
        el: '#form-search',
        data: {
            awsdate: daystr
        },
        methods: {
            submit: function (event) {
                event.preventDefault();
                htable.clear().draw();
                getApi(
                    '/cimiss/getawshistory/'+this.awsdate, {
                }, function (err, sjson) {
                    if (err) {
                        showError(err);
                    } else {
                        data2table(sjson)
                    }
                });
            },
            day_pre: function (event) {
                event.preventDefault();
                var s = moment(this.awsdate, 'YYYY-MM-DD').add('days', -1).format('YYYY-MM-DD');
                this.awsdate = s;
            },
            day_next: function (event) {
                event.preventDefault();
                var s = moment(this.awsdate, 'YYYY-MM-DD').add('days', 1).format('YYYY-MM-DD');
                this.awsdate = s;
            }
        }
    });


    function data2table(sjson) {
        var history_dataset = [];
        for(var sno in sjson){
            var sinfo = sjson[sno];
            var sname = sinfo["sname"];
            var machine = sinfo["machine"];
            var area = sinfo["area"];
            var county = sinfo["county"];
            var ctsarray = sinfo["cts"];
            var pqcarray = sinfo["pqc"];
            var regarray = sinfo["reg"];
            var batteryarray = sinfo["battery"];
            var h0_5 = array2ponit(pqcarray.slice(0,6), 'pqc') + array2ponit(ctsarray.slice(0,6), 'cts')+ array2ponit(regarray.slice(0,6), 'reg')+ array2ponit(batteryarray.slice(0,6), 'battery');
            var h6_11 = array2ponit(pqcarray.slice(6,12), 'pqc') + array2ponit(ctsarray.slice(6,12), 'cts')+ array2ponit(regarray.slice(6,12), 'reg')+ array2ponit(batteryarray.slice(6,12), 'battery');
            var h12_17 = array2ponit(pqcarray.slice(12,18), 'pqc') + array2ponit(ctsarray.slice(12,18), 'cts')+ array2ponit(regarray.slice(12,18), 'reg')+ array2ponit(batteryarray.slice(12,18), 'battery');
            var h18_23 = array2ponit(pqcarray.slice(18), 'pqc') + array2ponit(ctsarray.slice(18), 'cts')+ array2ponit(regarray.slice(18), 'reg')+ array2ponit(batteryarray.slice(18), 'battery');
            var history_row = [sno, sname, area, county, machine,
                '<div class="uk-text-nowrap">CTS质控</div><div class="uk-text-nowrap">CTS到报</div><div class="uk-text-nowrap">中心站</div><div class="uk-text-nowrap">电源电压</div>',
                h0_5, h6_11, h12_17, h18_23];
            history_dataset.push(history_row);
        }
        htable.rows.add(history_dataset).draw();
    }


    function array2ponit(arr, type){
        var domstr = '<div class="uk-flex uk-flex-center">';
        for(var i=0; i<arr.length; i++){
            if(type == 'cts' || type == 'pqc' || type == 'reg') {
                if(arr[i] == 1){
                    domstr = domstr + '<div class="circle-inner-yes"></div>';
                } else if (arr[i] == 0) {
                    domstr = domstr + '<div class="circle-inner-no"></div>';
                }
            } else if (type == 'battery') {
                if(arr[i] > 0){
                    domstr = domstr + '<div class="circle-inner-yes" uk-tooltip="title: ' + arr[i] + '"></div>';
                } else if(arr[i] <= 0) {
                    domstr = domstr + '<div class="circle-inner-no" uk-tooltip="title: ' + arr[i] + '"></div>';
                }
            }

        }
        domstr = domstr + '</div>'
        return domstr;
    }
});
