
$().ready(function() {
    if(localStorage.getItem('user_name') == null || localStorage.getItem('area_code') == null) {
        postApi('/iplogin', {
        }, function (err, result) {
            if (err) {
                showError(err);
            }
            else {
                if (result.succeed) {
                    localStorage.user_name = result.un;
                    localStorage.area_code = result.ac;
                } else {
                    showError('IP地址有误');
                    retrun;
                }
            }
        });
    }
})