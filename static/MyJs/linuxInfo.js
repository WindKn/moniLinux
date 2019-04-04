function editLinuxInfo(obj) {
    $('#editLinuxInfo').removeClass('hide');
    objTr = $(obj).closest("tr")
    serverName = objTr.find("td[name='serverName']").text();
    ip = objTr.find("td[name='ip']").text();
    port = objTr.find("td[name='port']").text();
    uname = objTr.find("td[name='uname']").text();
    pwd = objTr.find("td[name='pwd']").text();
    Path = objTr.find("td[name='Path']").text();
    serverID = objTr.find("td[name='serverID']").text();
    console.log(serverName, ip, port, uname, pwd, Path, serverID);
    $('#serverName').val(serverName);
    $('#ip').val(ip);
    $('#port').val(port);
    $('#uname').val(uname);
    $('#pwd').val(pwd);
    $('#Path').val(Path);
    $('#serverID').val(serverID);
}

function editSubmit() {
    debugger;
    serverName = $('#serverName').val();
    ip = $('#ip').val();
    port = $('#port').val();
    uname = $('#uname').val();
    pwd = $('#pwd').val();
    Path = $('#Path').val();
    serverID = $('#serverID').val();
    dataSend = {
        'serverName': serverName,
        'ip': ip,
        'port': port,
        'uname': uname,
        'pwd': pwd,
        'Path': Path,
        'serverID': serverID,
        'type': 'edit'
    };
    $.ajax({
            url: '/linuxInfo/',
            type: 'POST',
            data: dataSend,
            success: function (result) {
                debugger;
                var obj = JSON.parse(result);
                if (obj.status) {
                    location.reload();
                } else {
                    showError(obj.data);
                }
            }
        }
    )
}

function cancelEdit() {
    $('#editLinuxInfo').addClass('hide');
}

function deleteLinuxInfo(obj) {
    objTr = $(obj).closest("tr")
    serverID = objTr.find("td[name='serverID']").text();
    dataSend = {
        'serverID': serverID,
        'type': 'del'
    };
    $.ajax({
            url: '/linuxInfo/',
            type: 'POST',
            data: dataSend,
            success: function (result) {
                debugger;
                var obj = JSON.parse(result);
                if (obj.status) {
                    location.reload();
                } else {
                    showError(obj.data);
                }
            }
        }
    )
}

function showError(Msg) {
    debugger;
    $('#errMsg').text(Msg);
    $('#errMsg').removeClass('hide');
}


function addNewServer() {
    $('#addNewServer').removeClass('hide');
}
function cancelAdd() {
    $('#addNewServer').addClass('hide');
}

function addSubmit() {
    serverName = $('#serverNameAdd').val();
    ip = $('#ipAdd').val();
    port = $('#portAdd').val();
    uname = $('#unameAdd').val();
    pwd = $('#pwdAdd').val();
    Path = $('#PathAdd').val();
    serverID = $('#serverIDAdd').val();
    dataSend = {
        'serverName': serverName,
        'ip': ip,
        'port': port,
        'uname': uname,
        'pwd': pwd,
        'Path': Path,
        'serverID': serverID,
        'type': 'add'
    };
    $.ajax({
            url: '/linuxInfo/',
            type: 'POST',
            data: dataSend,
            success: function (result) {
                debugger;
                var obj = JSON.parse(result);
                if (obj.status) {
                    location.reload();
                } else {
                    showError(obj.data);
                }
            }
        }
    )
}