$(document).ready(function(){
  $("[name='sRespondD']").hide();
  $("[name='sRespondS']").hide();
  $("[name='rRespondD']").hide();
  $("[name='rRespondS']").hide();
  $("[name='sSubmit']").click(function(){
    $.post("{% url 'rt:login' %}",
      {
        username: $("[name='sUsername']").val(),
        password: $("[name='sPassword']").val(),
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
    function(res){
        var Obj= eval("("+res+")");//转换为json对象   
        if(Obj.status=="OK")
        {
            $("[name='sRespondD']").hide();
            $("[name='sRespondS']").show();
            $("[name='sRespondS']").text(Obj.status+": 欢迎回来~"+Obj.username);
            
          location.reload();
        }
        else if(Obj.err=="Login failed.")
        {
            $("[name='sRespondS']").hide();
            $("[name='sRespondD']").show();
            $("[name='sRespondD']").text(Obj.status+": 用户名与密码不匹配");
        }
        else
        {
            $("[name='sRespondS']").hide();
            $("[name='sRespondD']").show();
            $("[name='sRespondD']").text(Obj.status+": 请输入");
            $.each(Obj.detail,function(key,value){
            	$("[name='sRespondD']").append(key+" ");              
          	})
        }
    });
  });

  $("[name='rSubmit']").click(function(){
    $.post("{% url 'rt:register' %}",
      {
        username: $("[name='rUsername']").val(),
        password: $("[name='rPassword']").val(),
        password2: $("[name='rPassword2']").val(),
        email: $("[name='rEmail']").val(),
        name: $("[name='rName']").val(),
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
    function(res){
        var Obj= eval("("+res+")");//转换为json对象   
        if(Obj.status=="OK")
        {
            $("[name='rRespondD']").hide();
            $("[name='rRespondS']").show();
            $("[name='rRespondS']").text(Obj.status+": 欢迎来到我们的网站~"+Obj.username);
            
          location.reload();
        }
        else if(Obj.detail)
        {
          if(Obj.detail.password2=="Passwords not match.")
          {
              $("[name='rRespondS']").hide();
              $("[name='rRespondD']").show();
              $("[name='rRespondD']").text(Obj.status+": 密码不匹配");
          }
          else if(Obj.detail.email=="Enter a valid email address.")
          {
              $("[name='rRespondS']").hide();
              $("[name='rRespondD']").show();
              $("[name='rRespondD']").text(Obj.status+": 请输入合法的邮箱地址");
          }
          else
          {
              $("[name='rRespondS']").hide();
              $("[name='rRespondD']").show();
              $("[name='rRespondD']").text(Obj.status+": 请输入");
              $.each(Obj.detail,function(key,value){
                $("[name='rRespondD']").append(key+" "); 
              })
          }
        }
        else
        {
            $("[name='rRespondS']").hide();
            $("[name='rRespondD']").show();
            $("[name='rRespondD']").text(Obj.err);
        }
    });
  });

  $("[name='logout']").click(function(){
    $.get("{% url 'rt:logout' %}",     
      function(){
        location.reload();
    });
  });

});
