function viewLinuxInfo() {
    $('#detailInfo').removeClass('hide');
    $.ajax(
        {
            url: '/showmoni/',
            type: 'POST',
            data: {'serverID': $('#linuxID').val(), 'type': 'show'},
            success: function (data) {
                debugger;
                var obj = JSON.parse(data);
                cpuInfo(obj.timeList, obj.usr_cpu, obj.sys_cpu, obj.total_cpu);
                netInfo(obj.timeList, obj.recvList, obj.sendList, obj.total_dk);
                memInfo(obj.timeList, obj.mem_used, obj.mem_free, obj.mem_cache);
            }
        }
    )
}

function cpuInfo(lableTime, usr_cpu, sys_cpu, total_cpu) {
    $('#cpuInfo').remove(); // this is my <canvas> element
    $('#cpuInfoP').append('<canvas id="cpuInfo" width="591" height="295" class="chartjs-render-monitor"\n' +
        '                        style="display: block; width: 591px; height: 295px;"></canvas>');
    var cpuChart = $('#cpuInfo');
    if (cpuChart.length > 0) {
        new Chart(cpuChart, {
            type: 'line',
            data: {
                labels: lableTime,
                datasets: [{
                    label: 'usr cpu',
                    data: usr_cpu,
                    // backgroundColor: 'rgba(66, 165, 245, 0.5)',
                    borderColor: '#2196F3',
                    borderWidth: 1
                }, {
                    label: 'sys cpu',
                    data: sys_cpu,
                    // backgroundColor: '#40f34e',
                    borderColor: '#40f34e',
                    borderWidth: 1
                },
                    {
                        label: 'total cpu',
                        data: total_cpu,
                        // backgroundColor: '#40f34e',
                        borderColor: '#f5050a',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: '百分比'
                        },
                        ticks: {
                            beginAtZero: true,
                        }
                    }]
                }
            }
        });
    }
}

function netInfo(lableTime, recvList, sendList, total_dk) {
    $('#netInfo').remove(); // this is my <canvas> element
    $('#netInfoP').append('<canvas id="netInfo" width="591" height="295" class="chartjs-render-monitor"\n' +
        '                        style="display: block; width: 591px; height: 295px;"></canvas>');
    var netChart = $('#netInfo');
    if (netChart.length > 0) {
        new Chart(netChart, {
            type: 'line',
            data: {
                labels: lableTime,
                datasets: [{
                    label: '接受带宽',
                    data: recvList,
                    backgroundColor: 'rgba(66, 165, 245, 0.5)',
                    borderColor: '#2196F3',
                    borderWidth: 1
                }, {
                    label: '发送带宽',
                    data: sendList,
                    // backgroundColor: '#40f34e',
                    borderColor: '#110808',
                    borderWidth: 1
                }, {
                    label: '总带宽',
                    data: total_dk,
                    // backgroundColor: '#40f34e',
                    borderColor: '#f20005',
                    borderWidth: 1
                }
                ]
            },
            options: {
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'mbps'
                        },
                        ticks: {
                            beginAtZero: true,
                        }
                    }]
                }
            }
        });
    }
}

function memInfo(lableTime, mem_used, mem_free, mem_cache) {
    $('#memInfo').remove(); // this is my <canvas> element
    $('#memInfoP').append('<canvas id="memInfo" width="591" height="295" class="chartjs-render-monitor"\n' +
        '                        style="display: block; width: 591px; height: 295px;"></canvas>');
    var memChart = $('#memInfo');
    if (memChart.length > 0) {
        new Chart(memChart, {
            type: 'line',
            data: {
                labels: lableTime,
                datasets: [{
                    label: 'used mem',
                    data: mem_used,
                    // backgroundColor: 'rgba(66, 165, 245, 0.5)',
                    borderColor: '#0706f3',
                    borderWidth: 1
                }, {
                    label: 'free mem',
                    data: mem_free,
                    // backgroundColor: '#40f34e',
                    borderColor: '#f20005',
                    borderWidth: 1
                }, {
                    label: 'cache mem',
                    data: mem_cache,
                    // backgroundColor: '#40f34e',
                    borderColor: '#110808',
                    borderWidth: 1
                }
                ]
            },
            options: {
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'MB'
                        },
                        ticks: {
                            beginAtZero: true,
                        }
                    }]
                }
            }
        });
    }
}

function runTrace() {
    $.ajax(
        {
            url: '/linuxMon/',
            type: 'POST',
            data: {'server': $('#linuxID').val(), 'type': 'start'},
            success: function (result) {
                debugger;
                var obj = JSON.parse(result);
                $('traceInfo').removeClass('hide');
                $('#recordList').text(obj.tracedServer);
            }
        }
    )
}

function stopTrace() {
    $.ajax(
        {
            url: '/linuxMon/',
            type: 'POST',
            data: {'server': $('#linuxID').val(), 'type': 'stop'},
            success: function (result) {
                debugger;
                var obj = JSON.parse(result);
                $('traceInfo').removeClass('hide');
                $('#recordList').text(obj.tracedServer);
            }
        }
    )

}

function startTraceAll() {
    $.ajax(
        {
            url: '/linuxMon/',
            type: 'POST',
            data: {'type': 'start', 'server': 'all'},
            success: function (result) {
                debugger;
                var obj = JSON.parse(result);
                $('traceInfo').removeClass('hide');
                $('#recordList').text(obj.tracedServer);
            }
        }
    )
}

function stopAllTrace() {
    $.ajax(
        {
            url: '/linuxMon/',
            type: 'POST',
            data: {'type': 'stop', 'server': 'all'},
            success: function (result) {
                debugger;
                var obj = JSON.parse(result);
                $('traceInfo').removeClass('hide');
                $('#recordList').text(obj.tracedServer);
            }
        }
    )
}

function saveLinuxTraceInfo() {
    var saveName = $('#saveName').val();
    var serverID = $('#linuxID').val();
    $.ajax(
        {
            url: '/showmoni/',
            type: 'POST',
            data: {'type': 'save', 'saveName': saveName, 'serverID': serverID},
            success: function (result) {
                console.log('save success');
                $('#saveLinuxInfo').modal("hide");
                window.location.reload();
            }
        }
    )
}

function delHis() {
    var traceID = $('#traceList').val();
    $.ajax(
        {
            url: '/showMoniO/',
            type: 'POST',
            data: {'type': 'delHis', 'traceID': traceID},
            success: function (result) {
                location.reload();
            }
        }
    )

}

function showHis() {
    var traceID = $('#traceList').val();
    $.ajax(
        {
            url: '/showMoniO/',
            type: 'POST',
            data: {'type': 'showHis', 'traceID': traceID},
            success: function (data) {
                debugger;
                $('#detailInfo').removeClass('hide');
                var obj = JSON.parse(data);
                cpuInfo(obj.timeList, obj.usr_cpu, obj.sys_cpu, obj.total_cpu);
                netInfo(obj.timeList, obj.recvList, obj.sendList, obj.total_dk);
                memInfo(obj.timeList, obj.mem_used, obj.mem_free, obj.mem_cache);
            }
        }
    )
}

function selectTrcedLinux() {
    var serverID = $('#traceLinuxID').val();
    $.ajax(
        {
            url: '/linuxMoniO/',
            type: 'POST',
            data: {'serverID': serverID},
            success: function (data) {
                debugger;
                obj = JSON.parse(data);
                $("#traceList").empty();
                for (var i = 0; i < obj.value.length; i++) {
                    optString="<option value="+obj.valueID[i]+">"+obj.value[i]+"</option>";
                    $("#traceList").append(optString);
                }
            }
        }
    )
}

function filterShow() {
    $.ajax(
        {
            url: '/showMoniO/',
            type: 'POST',
            data: {'traceID': $('#traceList').val(), 'stime': $('#stime').val(), 'etime': $('#etime').val(),'type':'filterShow'},
            success: function (data) {
                debugger;
                $('#detailInfo').removeClass('hide');
                var obj = JSON.parse(data);
                cpuInfo(obj.timeList, obj.usr_cpu, obj.sys_cpu, obj.total_cpu);
                netInfo(obj.timeList, obj.recvList, obj.sendList, obj.total_dk);
                memInfo(obj.timeList, obj.mem_used, obj.mem_free, obj.mem_cache);
            }
        }
    )

}

function timeInterval() {
    $.ajax(
        {
            url: '/showMoniO/',
            type: 'POST',
            data: {'stime': $('#stime').val(), 'etime': $('#etime').val(),'type':'timeInterval'},
            success: function (data) {
                var obj = JSON.parse(data);
                $('#dtime').val(obj.dtime);
            }
        }
    )
}