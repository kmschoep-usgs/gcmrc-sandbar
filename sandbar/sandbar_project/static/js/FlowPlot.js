function FlowPlot(divId /* String */, gdawsSiteid) {
	
	this.graph = new Dygraph(divId, [], {});
	this.siteid = gdawsSiteid;
	
	this.update = function(startDate, endDate, params) {
		
		function formatParams(params) {
			var result = [];
			for (var i = 0; i < params.length; i++) {
				result.push({
					'name' : 'column[]', 
					'value' : 'inst!' + params[i].value + '!' + gdawsSiteid + '!' + params[i].name
				});
			}
		};
		
		var data = [{'name' : 'beginPosition', 'value' : startDate},
		            {'name' : 'endPosition', 'value' : endDate},
		            {'name' : 'column[]', 'value' : 'time!ISO!T'},
		            {'name' : 'tz', 'value' : '-7'},
		            {'name' : 'noDataFilter', 'value' : 'true'},
		            {'name' : 'output', 'value' : 'json'}]
		$.ajax({
			url: '/surveys/gdaws',
			data : data.concat(formatParams(params)),
			type : 'GET',
			complete : function(resp, status) {}
			
		})
	}
};