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
	// deal with area check boxes
	$('#area2d-chan-checkbox').prop('checked', false);
	$('#area2d-chan-checkbox').attr('disabled', true);
	$('#area2d-eddy_chan_sum-checkbox').prop('checked', false);
	$('#area2d-eddy_chan_sum-checkbox').attr('disabled', true);
	// deal with volume checkboxes
	$('#volume-chan-checkbox').prop('checked', false);
	$('#volume-chan-checkbox').attr('disabled', true);
	$('#volume-eddy_chan_sum-checkbox').prop('checked', false)
	$('#volume-eddy_chan_sum-checkbox').attr('disabled', true);
};

function enableChanTotalSite(checkboxID){
	var selector = '#' + checkboxID;
	$(selector).attr('disabled', false);
	$(selector).attr('disabled', false);
};


$(document).ready(function() {
	$(this).on('click', 'input[name="sb-param"], #sep-reatt', function() {
		var paramId = $(this).attr('id');
		var idStr = '#' + paramId;
		var checkedStatusSBParam = $(idStr).is(':checked');
		var checkedStatusSR = $('#sep-reatt').is(':checked');
		var parentVal = $(this).val();
		var dsMinVal = parseFloat($('#ds-min').val());
		if (dsMinVal < 8000) {
			chanEnableOkay = true;
		}
		else {
			chanEnableOkay = false;
		}
		selectDefaultSubParam(checkedStatusSBParam, parentVal);
		var sepReattChecked = $('#sep-reatt').is(':checked');
		//disable checkbox buttons if Area 2D is unchecked; enable if checked
		disableField(checkedStatusSBParam, parentVal);
		if (sepReattChecked) {
			disableChanTotalSite();
		}
		else if (!sepReattChecked && checkedStatusSBParam && chanEnableOkay) {
			//enableChanTotalSite();
		}
		else if (!sepReattChecked && checkedStatusSBParam && !chanEnableOkay) {
			disableChanTotalSite();
		}
		else {
			// do nothing
		}
	});
});
