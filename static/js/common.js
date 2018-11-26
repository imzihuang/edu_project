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
		success: function(msg) {console.log(msg);
			var msg = JSON.parse(msg);
			console.log(msg);
			school = msg.data[0].id;
			cardcode = msg.data[0].cardcode;
			console.log(school);
			console.log(cardcode);
		}
	})
}

//教师历史
$(".teacher_data_name").click(function(){console.log(2);
	$("#iframecontent").attr("src", "class.html");
});