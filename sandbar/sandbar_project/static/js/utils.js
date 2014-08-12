// get the value of an element
function get_value(element_id) {
	var elementValue = $(element_id).val();
	return elementValue;
};


function createErrorStr(missingParams) {
	var str = "";
	if (missingParams.length === 1) {
		str += missingParams[0]
	}
	else if (missingParams.length > 1) {
		for (j = 0; j < missingParams.length; j++) {
			
		}
	}
}