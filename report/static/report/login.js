'use strict';

function user_login() {
    var input_name = document.getElementById('username');
    var input_pwd = document.getElementById('input-password');
    var md5_pwd = document.getElementById('md5-password');
    md5_pwd.value = md5(input_pwd.value);
    $.get("check_user/", {"id": input_name.value, "pwd": input_pwd.value}, function (ret) {
        if (ret == 0) {
            window.location.href = "edit";
        } else {
            alert("login failed");
        }
    });
}