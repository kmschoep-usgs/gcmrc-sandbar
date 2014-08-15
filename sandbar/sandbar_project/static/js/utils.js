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
}