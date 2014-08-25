function selectDefaultSubParam(checkedStatus, parentVal) {
	var selectStr = 'div#' + parentVal + '-subgroup' + ' input:checkbox';
	var selectSubParamDefault = '#' + parentVal +'-eddy-checkbox';
	if (checkedStatus) {
		$(selectSubParamDefault).prop('checked', true);
	}
	else {
		$(selectStr).prop('checked', false);
	}
};

/*
function clearRadios(checkedStatus) {
	if (checkedStatus) {
		$('div.sub-param-group input:checkbox').prop('checked', false);
		var clickedTargetId = event.target.id
		var targetStr = '#' + clickedTargetId;
		$(targetStr).prop('checked', true);
	}
};
*/

function disableField(checkedStatus, parentVal) {
	var selectStr = 'div#' + parentVal + '-subgroup' + ' input:checkbox';
	if (checkedStatus) {
		$(selectStr).attr('disabled', false);
	}
	else {
		$(selectStr).attr('disabled', true);
	}
};

function disableChanTotalSite(){
	$('#area2d-chan-checkbox').attr('disabled', true);
	$('#area2d-eddy_chan_sum-checkbox').attr('disabled', true);
	$('#volume-chan-checkbox').attr('disabled', true);
	$('#volume-eddy_chan_sum-checkbox').attr('disabled', true);
};

function enableChanTotalSite(){
	$('#area2d-chan-checkbox').attr('disabled', false);
	$('#area2d-eddy_chan_sum-checkbox').attr('disabled', false);
	$('#volume-chan-checkbox').attr('disabled', false);
	$('#volume-eddy_chan_sum-checkbox').attr('disabled', false);
};


$(document).ready(function() {
	$(this).on('click', 'input[name="sb-param"]', function() {
		var checkedStatus = $(this).is(':checked');
		var parentVal = $(this).val();
		selectDefaultSubParam(checkedStatus, parentVal);
		//disable checkbox buttons if Area 2D is unchecked; enable if checked
		disableField(checkedStatus, parentVal);		
		if ($('#sep-reatt').is(':checked')) {
			disableChanTotalSite();
		}
		//else {
		//	enableChanTotalSite();
		//}
	});
});
