function controlDefaultSubParam() {
	$('div.sub-param-group input:checkbox').prop('checked', false);
};

function clearRadios(checkedStatus) {
	if (checkedStatus) {
		$('div.sub-param-group input:checkbox').prop('checked', false);
		var clickedTargetId = event.target.id
		var targetStr = '#' + clickedTargetId;
		$(targetStr).prop('checked', true);
	}
};

function disableField(checkedStatus) {
	if (checkedStatus) {
		$('div.sub-param-group input:checkbox').attr('disabled', false);
	}
	else {
		$('div.sub-param-group input:checkbox').attr('disabled', true);
	}
};

$(document).ready(function() {
	$(this).on('click', '#area2d-checkbox', function() {
		var checkedStatus = $('#area2d-checkbox').is(':checked');
		controlDefaultSubParam();
		//disable radio buttons if Area 2D is unchecked; enable if checked
		disableField(checkedStatus);		
	});
	/*
	$(this).on('click', 'div.sub-param-group input:checkbox', function() {
		var checkedStatus = $('#area2d-checkbox').is(':checked');
		// clear all the radio buttons and then populate the button that triggered the clear action
		clearRadios(checkedStatus);		
	});
	*/
})