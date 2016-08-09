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
	var strExistsArray = [];
	var result;
	for (i = 0; i < strArray.length; i++) {
		var fullStr = strArray[i];
		var subStrIndex = fullStr.indexOf(subString);
		if (subStrIndex > -1) {
			var strExists = true;
		}
		else {
			var strExists = false;
		}
		strExistsArray.push(strExists);
	}
	var trueIndex = strExistsArray.indexOf(true);
	if	(trueIndex > -1) {
		result = true;
	}
	else {
		result = false;
	}
	return result;
};