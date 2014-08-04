function selectDefaultSubParam(checkedStatus) {
	if (checkedStatus) {
		$('#area2d-eddy-radio').prop('checked', true);
	}
	else {
		$('div.sub-param-group input:radio').prop('checked', false);
	}
};

function clearRadios(checkedStatus) {
	if (checkedStatus) {
		$('div.sub-param-group input:radio').prop('checked', false);
		var clickedTargetId = event.target.id
		var targetStr = '#' + clickedTargetId;
		$(targetStr).prop('checked', true);
	}
};

function disableField(checkedStatus) {
	if (checkedStatus) {
		$('div.sub-param-group input:radio').attr('disabled', false);
	}
	else {
		$('div.sub-param-group input:radio').attr('disabled', true);
	}
};

$(document).on('click', '#area2d-checkbox', function() {
	var checkedStatus = $('#area2d-checkbox').is(':checked');
	selectDefaultSubParam(checkedStatus);
	//disable radio buttons if Area 2D is unchecked; enable if checked
	disableField(checkedStatus);
});

$(document).on('click', 'div.sub-param-group input:radio', function() {
	var checkedStatus = $('#area2d-checkbox').is(':checked');
	// clear all the radio buttons and then populate the button that triggered the clear action
	clearRadios(checkedStatus);
});