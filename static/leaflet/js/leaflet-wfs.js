L.wfs = L.Class.extend({
    options: {
        url: "",
        version: "1.1.0",
        srsName: "EPSG:3857",
        namespace: ""
    },
    initialize: function(url, options) {
        if (!url) {
            console.error('url of service is not defined', url);
        } else {
            this.url = url.indexOf('?service=wfs&') === -1 ? url + '?service=wfs': url;
            L.Util.setOptions(this, options);
            this._setBaseUrl();
        }
    },
    _setBaseUrl: function() {
        this.baseUrl = this.url + '&version=' + this.options.version;
    },
    getFeature: function(typeName, options, callback) {
        var url = this.baseUrl + '&request=GetFeature';
        if (typeName) {
            typeName = '&typeName=' + this.options.namespace +':' + typeName.join();
            var request = new L.wfs.feature(url, typeName, options, callback);
        } else {
            console.error('Forgot to set the typeName');
            callback(false, typeName);
        }
    },
    getCapabilities: function(callback) {
        var url = this.baseUrl + '&request=GetCapabilities',
            requestService = new L.wfs.request();
        requestService.makeRequest(url, 'GET', null, callback);
    },
    describeFeatureType: function() {

    },
    lockFeature: function() {

    },
    transaction: function() {

    }
});

L.WFS = function(url, options) {
    return new L.wfs(url, options);
};

L.wfs.feature = L.wfs.extend({
    options: {
        bbox: false,
        featureId: false,
        filter: false,
        maxFeatures: false,
        propertyName: false,
        outputFormat: "application/json"
    },
    initialize: function(url, typeName, options, callback) {
        this.url = url;
        this.typeName = typeName;
        L.Util.setOptions(this, options);
        var request = new L.wfs.request();

        request.makeRequest(this._setFinalUrl(), 'GET', null, callback);
        console.log(this._setFinalUrl());
    },
    _setFinalUrl: function() {
        var url = this.url + '&' + this.typeName,
            outputFormat = '&outputformat=' + this.options.outputFormat;

        url = this.options.bbox ?
        url + '&bbox='+this.options.bbox : this.options.featureId ?
        url + '&featureID='+this.options.featureId : this.options.filter ?
        url + '&filter='+this.options.filter : this.options.maxFeatures ?
        url + '&maxFeatures='+this.options.maxFeatures : this.options.propertyName ?
        url + '&bbox='+this.options.propertyName: url;

        return url + outputFormat;
    }
});

L.wfs.request = function() {
    /**
     * @param url    String
     * @param method String
     * @param params JSON.stringify | null
     * @param callback Callback
     */
    this.makeRequest = function(url, method, params, callback) {
        var request = new XMLHttpRequest();

        function _call() {
            request.open(method, encodeURI(url), true);
            request.onreadystatechange = function() {
                if (request.readyState == 4) {
                    if (request.status == 200) {
                        callback(request.responseText, false);
                    } else {
                        callback(false, request);
                    }
                }
            };
            request.send(params);
        }

        return _call();
    }
};