/**
 * Created by YangLiqiao on 2016/6/28.
 */

$(function() {
    $('#headbar li').removeClass('uk-active');
    if (location.pathname.indexOf('/cimiss')===0) {
        $('#cimiss').addClass('uk-active');
    } else if (location.pathname.indexOf('/page2')===0) {
        $('#page2').addClass('uk-active');
    }
    var x = ".uk-nav-default [href='" + location.pathname + "']";
    $(x).css("color", "#fff")
    $(x).parent().css("background-color", "#3a94e0")

    $(".tm-navbar-nav > li:not(.uk-active) > a").mouseover(function(){
        $(this).css("color","#fff");
    });

    $(".tm-navbar-nav > li:not(.uk-active) > a").mouseout(function(){
        $(this).css("color","rgba(255,255,255,0.8)");
    });

    $(".tm-navbar-nav > li > a").mouseover(function(){
        $(this).css("border-bottom","0.5px solid #fff");
    });

    $(".tm-navbar-nav > li > a").mouseout(function(){
        $(this).css("border-bottom","");
    });
});