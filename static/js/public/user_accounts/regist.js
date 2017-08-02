
//获取图形验证码
var code = ""
function get_image_code() {
    var d = new Date().getTime();
    var pre_code = code
    code = d;
    $(".get_image_code").attr("src", "/captcha?pre_code="+pre_code+"&code="+code);
    $(".captcha-code").attr("value",code);
}

//获取cookie
function getCookie(name) {
    var r = document.cookie.match(name + "=(.*);");
    return r[1]
}


$(document).ready(function(){
    get_image_code();

    //点击获取图形验证码
    $('#a_code').click(function () {
        get_image_code();
        //alert(getCookie("_xsrf"))
    });


    //点击获取手机验证码
    $('#captcha-btn').click(function (event) {
        //event.preventDefault();

        $(".mobile").focus(function () {
            $(".mobile-message").hide();
        });

        var mobile = $('.mobile').val();
        if(!mobile){
            $(".mobile-message").html("请输入手机号码！");
            $(".mobile-message").show();
            return;
        }

        var self = $(this);
        var timeCount = 60;
        //设置不能点击
        self.attr('disabled','disabled');
        // 设置当前倒计时
        var timer = setInterval(function () {
            self.text(timeCount);
            timeCount--;
            if(timeCount <= 0){
                self.text('获取验证码');
                self.removeAttr('disabled');
                clearInterval(timer);
            }
        },1000);
        // 发送ajax的请求

        var captcha = $('.captcha').val();

        $.ajax({
            url: '/mobilecode',
            type:"post",
            'data': {
                'mobile': mobile,
                'code': code,
                'captcha': captcha
            },
             'headers':{
                 "X-XSRFTOKEN":getCookie("_xsrf"),
             },
            'success': function (data) {
                if(data['status'] != 200){   //如果返回非200的状态
                     alert(data['message']);
                     get_image_code();
                     self.text('获取验证码');          //
                     self.removeAttr('disabled');
                     clearInterval(timer);
                }else{
                    get_image_code();
                    alert( '验证码已发送至'+data['message']+'，请注意查收！');
                }
            }
        });
    });
});