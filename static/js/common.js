//获取学校id
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
		}
	})
}