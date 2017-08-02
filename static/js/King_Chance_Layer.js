// JavaScript Document
$(document).ready(function(){
	var $King_Chance_LayerCont = $(".King_Chance_LayerCont");
	var $King_Chance_Layer_Close = $(".King_Chance_Layer_Close");
	var $King_Chance_Layer_Btn = $(".King_Chance_Layer_Btn > ul > li");
	var $King_Chance_Layer_Content = $(".King_Chance_Layer_Content > ul > li");
	var King_Chance_Layer_Btn_Hover = "hover";
	var King_Chance_Layer_Show_Num = 0;
	var King_Chance_Layer_Btn_Len = $King_Chance_Layer_Btn.length;
	$King_Chance_Layer_Btn.hover(function(){
		var King_Chance_Layer_Show_Num = $King_Chance_Layer_Btn.index(this);
		$(this).addClass(King_Chance_Layer_Btn_Hover).siblings().removeClass(King_Chance_Layer_Btn_Hover);
		$King_Chance_Layer_Content.eq(King_Chance_Layer_Show_Num).show().siblings().hide();
		$King_Chance_Layer_Content.eq(King_Chance_Layer_Show_Num).find("img").lazyload();
		});
	var King_Chance_Layer_Play = function(){
		King_Chance_Layer_Show_Num++;
		if(King_Chance_Layer_Show_Num>=King_Chance_Layer_Btn_Len) King_Chance_Layer_Show_Num=0;
		$King_Chance_Layer_Btn.eq(King_Chance_Layer_Show_Num).addClass(King_Chance_Layer_Btn_Hover).siblings().removeClass(King_Chance_Layer_Btn_Hover);
		$King_Chance_Layer_Content.eq(King_Chance_Layer_Show_Num).show().siblings().hide();
		};
	$King_Chance_Layer_Close.click(function(){clearInterval(King_Chance_Layer_Play_Time);$King_Chance_LayerCont.slideUp();});
	King_Chance_Layer_Pop = function(){
		$King_Chance_LayerCont.slideDown();
		$King_Chance_Layer_Btn.eq(King_Chance_Layer_Show_Num).addClass(King_Chance_Layer_Btn_Hover);
		$King_Chance_Layer_Content.eq(King_Chance_Layer_Show_Num).show();
		King_Chance_Layer_Play_Time = setInterval(function(){King_Chance_Layer_Play();},2000);
		};
	});
function King_Chance_Layer_Probability(){
	if(window.addEventListener)	{
		window.addEventListener("load",King_Chance_Layer_Pop,false);
	}else{
		window.attachEvent("onload",King_Chance_Layer_Pop);
	};
};
