/**
 * Created by YangLiqiao on 2017/6/16.
 */
$(document).ready(function() {
    var map = L.map('map').setView([27.40, 116.1], 7);

    //getApi(
    //    '', {
    //}, function (err, result) {
    //    if (err) {
    //    }
    //    else {
    //
    //    }
    //});

    L.tileLayer('http://10.116.32.88/mapserver.php?t=t&x={x}&y={y}&z={z}', {
            attribution: '&copy; <a>江西省气象信息中心</a> contributors'
    }).addTo(map);


    new L.WFS({
        url: 'http://10.116.32.244:8080/geoserver/jiangxi/ows',
        typeNS: 'jiangxi',
        typeName: 'jx_outer',
        crs: L.CRS.EPSG4326,
        geometryField: 'the_geom',
        style: {
          color: 'black',
          weight: 0.5
        }
    }).addTo(map);

    new L.WFS({
        url: 'http://10.116.32.244:8080/geoserver/jiangxi/ows',
        typeNS: 'jiangxi',
        typeName: 'jx_all',
        crs: L.CRS.EPSG4326,
        geometryField: 'the_geom',
        style: {
          color: 'black',
          weight: 0.5
        }
    }).addTo(map);

    var meteoPoints = [
        [ 27.11285 , 116.222309, 1, 190], //Ipsach
        [ 27.085272, 116.20377 , 5, 90], //Mörigen
        [ 27.092285, 116.156734, 3, 170], //Twann
        [ 27.13294 , 116.220936, 10, 45], //Vingelz
        [ 27.088311, 116.128925, 19 , 280], //Twannberg
        [ 27.124765, 116.234669, 21, 135], //Nidau
        [ 27.055107, 116.07159 , 25 , 360 ]  //lelanderon
    ];

    meteoPoints.forEach(function(p){
        var icon = L.WindBarb.icon({deg: p[3], speed: p[2], pointRadius:2, strokeWidth:2});
        var marker = L.marker([p[0],p[1]], {icon: icon}).addTo(map).bindPopup("<p>Wind Speed: "+p[2]+"</p>"+
                                                                              "<p>Wind Direction: "+p[3]+"</p>");
    });

});