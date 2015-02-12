function createLink(site_id, ds_min, ds_max, paramArry) {
	var queryStr = '';
	var parentParams = '';
	for (z = 0; z < paramArry.length; z++) {
		var parentParam = paramArry[z].paramVal;
		parentParams += '&param_type=' + parentParam;
		var calc_type = paramArry[z].subParamVals;
		for (x = 0; x < calc_type.length; x++) { 
			var paramCalcType = '&' + parentParam + '_calc_type=';
			queryStr += paramCalcType + calc_type[x];
		}
	}
	var queryURL = SB.DATA_DOWNLOAD + '?site_id=' + site_id + parentParams + '&ds_min=' + ds_min + '&ds_max=' + ds_max + queryStr + '&download=true';
	return queryURL;
};