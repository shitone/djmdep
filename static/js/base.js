/**
 * Created by YangLiqiao on 2016/6/28.
 */

$(function() {
    $('#headbar li').removeClass('active');
    if (location.pathname.indexOf('/cimiss')===0) {
        $('#cimiss').addClass('active');
    } else if (location.pathname.indexOf('/product')===0) {
        $('#product').addClass('active');
    }
    // var x = ".uk-nav-default [href='" + location.pathname + "']";
    // $(x).css("color", "#fff");
    // $(x).parent().css("background-color", "#3a94e0");

    $(".my-navbar-nav > li:not(.active) > a").mouseover(function(){
        $(this).css("color","#fff");
    });

    $(".my-navbar-nav > li:not(.active) > a").mouseout(function(){
        $(this).css("color","rgba(255,255,255,0.8)");
    });

    $(".my-navbar-nav > li > a").mouseover(function(){
        $(this).css("border-bottom","0.5px solid #fff");
    });

    $(".my-navbar-nav > li > a").mouseout(function(){
        $(this).css("border-bottom","");
    });
});