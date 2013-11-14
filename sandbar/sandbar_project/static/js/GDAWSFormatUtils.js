SB.GDAWSFormatUtils = {
	getDygraphCSV : function(jsonResp, dataKey, dataLabel) {
		var LF = '\n';
		var result = 'Time,' + dataLabel + LF;
		
		var data = jsonResp.success.data;
		
		for (var i = 0; i < data.length; i++) {
			result += data[i].time + ',' + data[i][dataKey] + LF;
		}
		
		return result;
	},
	getDataQueryString : function(gdawsSiteId, startDate, endDate, params) {
		var paramsData = '';
		for (var i = 0; i < params.length; i++) {
			var thisConfig = SB.Config.SITE_PARAMETERS[params[i]];
			paramsData += '&column[]=inst!' + thisConfig.groupName +  '!' + gdawsSiteId + '!' + thisConfig.colName;
		}
		return 'beginPosition=' + startDate + '&endPosition=' + endDate + 
			'&column[]=time!ISO!time' + paramsData +
			'&tz=-7&noDataFilter=true&output=json';
	}
}