//获取cookie
function getCookie(name) {
    var r = document.cookie.match(name + "=(.*);");
    return r[1]
}

$(document).ready(function () {
    //发送说说
    $(":submit").click(function () {
        var options = {
          success: function () {
            location.reload();
          }
        };
        $("#message").ajaxForm(options);
    });
    //显示评论框
    $(".pinglun-btn").click(function(){
        var id = "#"+$(this).attr("data-id");
        $(id).toggle(500);
    });

    //
    // //提交评论
    $(".comment-btn").click(function () {
        var id = "#"+$(this).attr("data-id");
        var options = {
          success: function (data) {
              if(data['status'] != 200){   //如果返回非200的状态
                  alert(data['message']);
                }else{
                  $(id).toggle(500);
                  $(".p-text-area").val("")
                  location.reload();
                }
          }
        };
        $(".comment-form").ajaxForm(options);
    });
});



