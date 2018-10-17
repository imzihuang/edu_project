function jumpPages() {
		var allCount = parseInt(document.getElementById("jumpPageCount").value);
		var ele=document.getElementById("jumpPage");
		var arg = ele.value;
		var url = document.getElementById("jumpPageUrl").value;
		if (arg == null || arg.replace(/\ /g, "") == "") {
			return false;
		} else if (isNaN(arg)) {
			alert("请输入数字！");
			ele.focus();
		} else {
			var inputCount = parseInt(arg);
			if (inputCount <= 0) {
				inputCount = 1;
			} else if (inputCount > allCount) {
				inputCount = allCount;
			}
			location.href = url + "pageIndex=" + inputCount;
		}
	}