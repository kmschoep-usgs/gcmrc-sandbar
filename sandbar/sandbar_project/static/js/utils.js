// get the value of an element
function get_value(element_id) {
	var elementValue = $(element_id).val();
	return elementValue;
};

function createPlotDates(dateStr, altDateStr) {
	if (dateStr != null) {
		plotDate = dateStr;
	}
	else if (altDateStr != null) {
		plotDate = altDateStr;
	}
	else {
		plotDate = null;
	}
	return plotDate;
};

function collect() {
	var ret = {};
	var len = arguments.length;
	for (var i = 0; i < len; i++) {
		for (p in arguments[i]) {
			ret[p] = arguments[i][p]
		}
	}
	return ret;
};

function searchForSubString(subString, strArray) {
	for (i = 0; i < strArray.length; i++) {
		var value = strArray[i];
		
	}
};