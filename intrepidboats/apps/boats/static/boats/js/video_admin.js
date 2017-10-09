$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href); // eslint-disable-line
	return results[1] || 0;
};

$(document).ready(function () {
    if($.urlParam('_from') == 'article'){
        $('.form-row.field-boat').hide();
    }
});