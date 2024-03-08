	(function($) {
		"use strict";
	
	
	$(document).ready(function() {
	

	/*scroll to top*/
	$(window).scroll(function() {
	if ($(this).scrollTop() > 100) {
	$('.scrollup').fadeIn();
	} else {
	$('.scrollup').fadeOut();
	}
	});
	
	$('.scrollup').on("click",function() {
	$("html, body").animate({
	scrollTop: 0
	}, 500);
	return false;
	
	});
	
	
	$(".accordion_example").smk_Accordion({
            showIcon: true, //boolean
            animation: true, //boolean
            closeAble: false, //boolean
            slideSpeed: 200 //integer, miliseconds
        });
	
	
	
	
	
		});
	
	})(jQuery);