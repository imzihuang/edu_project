//获取学校id
var school;
var cardcode;

function schoolInput() {
	var data = {
		"limit": 20,
		"offset": 1,
	}
	$.ajax({
		type: "GET",
		contentType: "application/x-www-form-urlencoded;chartset=UTF-8",
		url: "/school/infos",
		async: false,
		data: data,
		timeout: "30000",
		success: function(msg) {
			var msg = JSON.parse(msg);
			console.log(msg);
			school = msg.data[0].id;
			cardcode = msg.data[0].cardcode;
			console.log(school);
			console.log(cardcode);
		}
	})
}

//全选按钮
$("#zx_checkedAllBtn").click(function() {
	if(this.checked) {
		$("#tbody :checkbox").prop("checked", true);
	} else {
		$("#tbody :checkbox").prop("checked", false);
	}
	allchk();
});

$("#tbody :checkbox").click(function() {
	allchk();
})

//全选
function allchk() {
	$('#delInfo').attr("disabled", false);
	var chknum = $("#tbody :checkbox").size();
	var chk = 0;
	var trLength = $("#tbody tr").length;
    for(var i=0;i<trLength;i++){
    	if($("#tbody tr").eq(i).find('input').is(':checked')){
    	    chk++;
    	}
    }console.log(chk);console.log(chknum);
	if(chknum == chk) {
		$("input[name=allcheck]").prop("checked", true);
	} else {
		$("input[name=allcheck]").prop("checked", false);
	}
	if(chk >= 1) {
		$('#delInfo').attr('class', 'btn btn-primary btn-myown');
	} else {
		$('#delInfo').attr('class', 'btn btn-default btn-myown');
	}
}