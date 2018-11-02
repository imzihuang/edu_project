$.extend({
	majax:function(){
	 var defaultOption = {
	 	url:"",
	 	jsonpCallback:'',
	 	timeout:"30000",
	 	contentType: "application/x-www-form-urlencoded;chartset=UTF-8",
	 	data:{},
	 	successCallBack:function() {},
	 	errorCallBack:function() {},
	 }
	 $.ajax({
	 	url:defaultOption.url,
	 	data:defaultOption.data,
	 	xhrFields: {
	 		"withCredentials": true
	 	},
	 	type: 'POST',
	 	jsonpCallback:defaultOption.jsonpCallback,
	 	traditional: true,
	 	contentType: defaultOption.contentType,
	 	dataType: 'json',
	 	cache: false,
	 	timeout:defaultOption.timeout,
	 	success:function(data){
	 		defaultOption.successCallBack(data);
	 	},
	 	error:function(data){
	 		defaultOption.errorCallBack(data);
	 	}
	 });
    }
});

