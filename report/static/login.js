'use strict';

function checkForm() {
    var input_name = document.getElementById('username');
    var input_pwd = document.getElementById('input-password');
    var md5_pwd = document.getElementById('md5-password');
    md5_pwd.value = md5(input_pwd.value);
    return true;
}