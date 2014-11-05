SB.GDAWSFormatUtils = {
	getDygraphCSV : function(jsonResp, dataKey, dataLabel, sandbarStart) {
		var LF = '\n';
		var result = 'Time,' + dataLabel + LF;
		var sbDateStart = Date.parse(sandbarStart);
		var data = jsonResp.success.data;
		var dataStartTime = data[0].time; // get the earliest time from the returned data set
		var dataStartTimeParse = Date.parse(dataStartTime);
		if (sbDateStart < dataStartTimeParse) {
			result += sandbarStart + ',' + 'NaN' + LF; // ensure that discharge or sediment plot has the same x-axis domain as the sandbar survey data
		}
		for (var i = 0; i < data.length; i++) {
			result += data[i].time + ',' + data[i][dataKey] + LF;
		}
		return result;
	},
	getDataQueryString : function(gdawsSiteId, dischargeSite, startDate, endDate, params) {
		var paramsData = '';
		var paramsArray = [];
		for (var i = 0; i < params.length; i++) {
			var thisConfig = SB.Config.SITE_PARAMETERS[params[i]];
			/* create param string for the correct sediment site */
			if (thisConfig.colName === 'cumulLoad' && thisConfig.site === gdawsSiteId) {
				paramsData += '&column[]=inst!' + thisConfig.groupName +  '!' + gdawsSiteId + '!' + thisConfig.colName;
			}
			/* create param string for the correct discharge site */
			if (thisConfig.colName === 'discharge' && thisConfig.site === dischargeSite) {
				paramsData += '&column[]=inst!' + thisConfig.groupName +  '!' + dischargeSite + '!' + thisConfig.colName;
			}
			paramsArray.push(paramsData);
		}
		completeParamsStr = paramsArray.join('');
		return 'beginPosition=' + startDate + '&endPosition=' + endDate + 
			'&column[]=time!ISO!time' + completeParamsStr +
			'&every=P1M&tz=-7&noDataFilter=true&output=json&downscale=PT24H';
	}
}