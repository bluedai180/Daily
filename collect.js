var json_text = "{\n" +
    "  \"info\": [\n" +
    "    [\n" +
    "      \"HP55C74\",\n" +
    "      \"需求分析实现\",\n" +
    "      \"123\",\n" +
    "      \"111111111111111111111111\",\n" +
    "      \"1\",\n" +
    "      \"\",\n" +
    "      \"\",\n" +
    "      \"入库\",\n" +
    "      \"原始问题\",\n" +
    "      \"aaa\",\n" +
    "      \"2017/12/13\",\n" +
    "      \"qqqqqqqqqqqqqqq\"\n" +
    "    ],\n" +
    "    [\n" +
    "      \"VEH-CM7\",\n" +
    "      \"解决bug\",\n" +
    "      \"456\",\n" +
    "      \"222222222222222222222222\",\n" +
    "      \"2\",\n" +
    "      \"\",\n" +
    "      \"\",\n" +
    "      \"转其他组\",\n" +
    "      \"原始问题\",\n" +
    "      \"bbb\",\n" +
    "      \"2017/12/13\",\n" +
    "      \"wwwwwwwwwwwwwww\"\n" +
    "    ],\n" +
    "    [\n" +
    "      \"YL50B71\",\n" +
    "      \"团队建设\",\n" +
    "      \"789\",\n" +
    "      \"333333333333333333333333\",\n" +
    "      \"3\",\n" +
    "      \"\",\n" +
    "      \"\",\n" +
    "      \"非问题\",\n" +
    "      \"新需求\",\n" +
    "      \"ccc\",\n" +
    "      \"2017/12/13\",\n" +
    "      \"eeeeeeeeeeeeeee\"\n" +
    "    ]\n" +
    "  ]\n" +
    "}";


var collection = document.getElementById("collection");
var json_obj = JSON.parse(json_text);
for (var i = 0; i < json_obj.info.length; i++) {
    var line = document.createElement("tr");
    for (var j = 0; j < json_obj.info[0].length;j++) {
        var cell = document.createElement("td");
        cell.innerText = json_obj.info[i][j];
        line.appendChild(cell);
    }
    collection.appendChild(line);
}

function download() {
    
}

function send() {
    
}