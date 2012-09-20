$(document).ready(function(){
    $("#main-nav li ul").hide();

    $("#main-nav li a.current").parent().find("ul").slideToggle("slow");

    $("#main-nav li a.nav-top-item").click(
        function () {
            $(this).parent().siblings().find("ul").slideUp("normal");
            $(this).parent().siblings().find("a.current").removeClass("current");
            $(this).toggleClass("current");
            $(this).next().slideToggle("normal");
            return false;
        });
    
    $("#main-nav li .nav-top-item").hover(
        function () {
            $(this).stop().animate({ paddingRight: "25px" }, 200);
        }, 
        function () {
            $(this).stop().animate({ paddingRight: "15px" });
        });
    
    $(".content-box-header h3").click(
        function () {
            $(this).parent().next().toggle();
        });

    $('.content-box .content-box-content div.tab-content').hide();
    $('ul.content-box-tabs li a.default-tab').addClass('current');
    $('.content-box-content div.default-tab').show();
    
    $('.content-box ul.content-box-tabs li a').click(
        function() { 
            $(this).parent().siblings().find("a").removeClass('current');
            $(this).addClass('current');
            var currentTab = $(this).attr('href');
            $(currentTab).siblings().hide();
            $(currentTab).show();
            return false; 
        });
    
    $('#tab2 div.student').hide();
    $('#tab2 div.admin').hide();
    $('#tab2 div.statistician').hide();
    
    $('#tab2 div.options input').click(
        function(){
            var $name = $(this).attr('name');
            
            if( $name == "superadmin"){
                $('#tab2 div.student').hide();
                $('#tab2 div.admin').toggle();
                $('#tab2 div.statistician').hide();
            }else if($name == "statistician"){
                $('#tab2 div.student').hide();
                $('#tab2 div.admin').hide();
                $('#tab2 div.statistician').toggle();
            }else if($name == "student"){
                $('#tab2 div.student').toggle();
                $('#tab2 div.admin').hide();
                $('#tab2 div.statistician').hide();
            }
            
            $(this).siblings().removeAttr("checked");
        });
    
    $('#tab1 thead input').click(
        function(){
            $(this).parent().parent().parent().siblings("tbody").find("input[type='checkbox']").attr('checked', $(this).is(':checked'));
        });
    
    $('#tab1 tbody td.edit').dblclick(
        function(){
            $('.content-box ul.content-box-tabs li a').click();
            var $role = $(this).next().text();
            
            if($role == "管理员"){
                $("#tab2 div.options input[name='superadmin']").click();
                $('#tab2 div.admin input[name="admin-name"]').val($(this).text());
                $('#tab2 form #userid').val($(this).prev().children('input[type="checkbox"]').attr('name'));
            }else if($role == "记录员"){
                $("#tab2 div.options input[name='statistician']").click();
                $('#tab2 div.statistician input[name="statistician-name"]').val($(this).text());
                $('#tab2 form #userid').val($(this).prev().children('input[type="checkbox"]').attr('name'));
            }else{
                $("#tab2 div.options input[name='student']").click();
                $('#tab2 form #userid').val($(this).prev().children('input[type="checkbox"]').attr('name'));
                $('#tab2 div.student input[name="student-name"]').val($(this).text());
                $('#tab2 div.student input[name="schoolid"]').val($(this).next().next().text());
                $('select[name="sex"]').val($(this).next().next().next().text());
            }
        });
});
