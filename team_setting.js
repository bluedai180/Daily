var json_text = "{\n" +
    "  \"member\":[\n" +
    "    \"aaa\",\n" +
    "    \"bbb\",\n" +
    "    \"ccc\"\n" +
    "  ]\n" +
    "}";

var member = document.getElementById("member");
var authority = document.getElementById("authority");
var json_obj = JSON.parse(json_text);

for (var i = 0; i < json_obj.member.length; i++) {
    var line = document.createElement("tr");
    var names = document.createElement("td");
    var option = document.createElement("td");
    var btn = document.createElement("input");
    btn.type = "button";
    btn.onclick = function () {
        this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);
    };
    btn.value = "delete";
    names.innerText = json_obj.member[i];
    line.appendChild(names);
    option.appendChild(btn);
    line.appendChild(option);
    member.appendChild(line);
}

function save() {
    var username = document.getElementById("user_name");
    var pwd = document.getElementById("pwd");
    var line = document.createElement("tr");
    var names = document.createElement("td");
    var option = document.createElement("td");
    var btn = document.createElement("input");
    btn.type = "button";
    btn.onclick = function () {
        this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);
    };
    btn.value = "delete";
    names.innerText = username.value;
    line.appendChild(names);
    option.appendChild(btn);
    line.appendChild(option);
    member.appendChild(line);
}