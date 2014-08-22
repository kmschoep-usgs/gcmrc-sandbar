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
			if (parentParam === 'volume') {
				var eBars = true;
				var plotter = [SB.DotPlotter, Dygraph.Plotters.linePlotter];
			}
			else {
				var eBars = false;
				var plotter = null;
			}
			var displayName = params[j].displayName;
			var paramUnit = params[j].paramUnit;
			var yAxisLabel = 'Sandbar ' + displayName + ' (' + paramUnit + ')';
			var calc_type = params[j].subParamVals;
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
							highlightCircleSize: 4,
							drawPoints: true,
							pointSize: 3,
							customBars: eBars,
							plotter: plotter
						});
						if (columnCount < calc_type.length) {
							var missingDataArr = [];
							if ($.inArray('Eddy Total', headerArray) == -1 && $.inArray('eddy', calc_type) > -1) {
								missingDataArr.push('Eddy'); 
							}
							if ($.inArray('Channel Total', headerArray) == -1 && $.inArray('chan', calc_type) > -1) {
								missingDataArr.push('Channel'); 
							}
							if ($.inArray('Total Site', headerArray) == -1 && $.inArray('eddy_chan_sum', calc_type) > -1) {
								missingDataArr.push('Total Site'); 
							}
							var missingDataStr = missingDataArr.join(', ');
							var errorDisplay = '<p class="param-missing"> The following ' + displayName + ' parameters are unavailable for this site: ' + missingDataStr + '.</p>';
							graphDivEl(parentParam).append(errorDisplay);
							$('<br/>').insertAfter(graphDivEl(parentParam));
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