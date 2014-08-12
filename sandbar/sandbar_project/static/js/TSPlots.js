SB.TSPlots = function (graphsDivId /* id of div containing the divs for each parameter's graph */, siteId /* String */) {
	this.graphsDivEl = $('#' + graphsDivId);
	this._graphs = {}; // Holds current dygraphs
	this.siteId = siteId;
	
	var graphId = function(key) {
		return key + '-graph-div';
	}
	var graphDivEl = function(key) {
		return $('#' + graphId(key));
	};
	//var graphDivEl = $('#timeseries-plot');
	// public object methods
	this.updatePlots = function(dischargeMin, dischargeMax /* String discharge inputs */, params, gcmrcPlots, totalParams) {
		var gcmrcPlots = gcmrcPlots;
		var graphs = {};
		var currentGraphs = [];
		for (j = 0; j < params.length; j++) {
			var parentParam = params[j].paramVal;
			var displayName = params[j].displayName;
			var paramUnit = params[j].paramUnit;
			var yAxisLabel = 'Sandbar ' + displayName + ' (' + paramUnit + ')';
			var calc_type = params[j].subParamVals;
			console.log(calc_type);
			var calcTypeParamStr = '';
			for (i = 0; i < calc_type.length; i++) {
				calcTypeParamStr += '&calc_type=' + calc_type[i];
			}
			
			this.graphsDivEl.children('#plots-loading-div').show();
			$.ajax({
				url: SB.AREA_2D_URL,
				async: false,
				type: 'GET',
				data: 'site_id=' + this.siteId + '&param_type=' + parentParam + '&ds_min=' + dischargeMin + '&ds_max=' + dischargeMax + calcTypeParamStr,
				context : this,
				complete : function(resp, status) {
					this.graphsDivEl.children('#plots-loading-div').hide();
					if (status === 'success') {
						currentGraphs.push(parentParam);
						/* destroy previously created graphs */
						for (key in this._graphs) {
							var currentGraphExists = $.inArray(key, currentGraphs);
							try {
								if (currentGraphExists === -1) {
									graphDivEl(key).hide();
									this._graphs[key].destroy();									
								}
								else {
									//do nothing
								}
							}
							catch(TypeError) {
								continue;
							}
						}
						for (key in gcmrcPlots) {
							var currentGraphExists = $.inArray(key, totalParams);
							try {
								if (currentGraphExists === -1) {
									graphDivEl(key).hide();
									this._graphs[key].destroy();									
								}
								else {
									//do nothing
								}
							}
							catch(TypeError) {
								continue;
							}
						}
						// Update the selected graphs
						var data = resp.responseText;
						var csvHeader = data.slice(0, data.indexOf('\n'));
						var csvHeaderLineBreak = csvHeader.replace(/(\r\n|\n|\r)/gm,""); //remove line breaks
						var headerArray = csvHeaderLineBreak.split(",");
						console.log(headerArray);
						console.log($.inArray("Eddy", headerArray));
						console.log($.inArray('eddy', calc_type));
						var columnCount = headerArray.length - 1;
						graphDivEl(parentParam).show();
						graphs[parentParam] = new Dygraph(graphId(parentParam),
								data, {
							xlabel: "Date",
							ylabel: yAxisLabel,
							yAxisLabelWidth: 95,
							labelsDivWidth: 300,
							showRangeSelector: true,
							legend: 'always',
							strokePattern: [5, 5],
							drawPoints: true,
							pointSize: 3
						});
						if (columnCount < calc_type.length) {
							var missingDataStr = '';
							if ($.inArray('Eddy', headerArray) == -1 && $.inArray('eddy', calc_type) > -1) {
								missingDataStr += 'Eddy '; 
							}
							if ($.inArray('Channel', headerArray) == -1 && $.inArray('chan', calc_type) > -1) {
								missingDataStr += 'Channel '; 
							}
							if ($.inArray('Total Site', headerArray) == -1 && $.inArray('eddy_chan_sum', calc_type) > -1) {
								missingDataStr += 'Total Site '; 
							}
							var errorDisplay = '<p>' + missingDataStr + 'data is unavailable from our database.</p>'
							graphDivEl(parentParam).append(errorDisplay);							
						}
					}
					else {
						alert('Unable to retrieve data: ' + resp.status + ' : ' + resp.statusText);
					}
				}
			});					
		}
		this._graphs = graphs;
	};
};