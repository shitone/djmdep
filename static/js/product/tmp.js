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

    var imageUrl = '/static/media/111.png',
    imageBounds = [[0, 73], [60, 153]];
    L.imageOverlay(imageUrl, imageBounds, {opacity:0.7}).addTo(map);

});