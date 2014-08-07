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

function clearRadios(checkedStatus) {
	if (checkedStatus) {
		$('div.sub-param-group input:checkbox').prop('checked', false);
		var clickedTargetId = event.target.id
		var targetStr = '#' + clickedTargetId;
		$(targetStr).prop('checked', true);
	}
};

function disableField(checkedStatus, parentVal) {
	var selectStr = 'div#' + parentVal + '-subgroup' + ' input:checkbox';
	if (checkedStatus) {
		$(selectStr).attr('disabled', false);
	}
	else {
		$(selectStr).attr('disabled', true);
	}
};

$(document).ready(function() {
	$(this).on('click', 'input[name="sb-param"]', function() {
		var checkedStatus = $(this).is(':checked');
		var parentVal = $(this).val();
		selectDefaultSubParam(checkedStatus, parentVal);
		//disable checkbox buttons if Area 2D is unchecked; enable if checked
		disableField(checkedStatus, parentVal);		
	});
	/*
	$(this).on('click', 'div.sub-param-group input:checkbox', function() {
		var checkedStatus = $('#area2d-checkbox').is(':checked');
		// clear all the radio buttons and then populate the button that triggered the clear action
		clearRadios(checkedStatus);		
	});
	*/
})