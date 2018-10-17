window.onload=function(){
	function height(){
	    		var height=$(window).height();
	    		$('#iframecontent').height(height-90);
	    	}
			height();
	
	    	$(window).resize(function(){
	    			height();
	    	});
	    	
	    	/*$('.clickBtn').click(function(){
	    		$(this).attr('src','sendInfoDetail.html'))
	    	});*/
	    	$('.nowAct').click(function(){
					//alert('aaaa');
					$(this).addClass('current').siblings('li').removeClass('current');
				});
	  };
