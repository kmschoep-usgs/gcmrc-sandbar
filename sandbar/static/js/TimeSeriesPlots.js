function graphDivEl(graphsDivId) {
	var str = $('#' + graphsDivId);
	return str;
};

function graphId(key) {
	return $('#' + graphId(key));
};

function TimeSeriesPlot(options) {
	 var url = options.url;
	 var siteID = options.siteID;
	 var parentParam = options.parentParam;
	 var dischargeMin = options.dischargeMin;
	 var dischargeMax = options.dischargeMax;
	 var calcTypeParamStr = options.calcTypeParamStr;
	 var graphChildren = options.graphChildren;
	 var gcmrcPlots = options.gcmrcPlots;
	 var totalParams = options.totalParams;
	 var yAxisLabel = options.yAxisLabel;
	 var eBars = options.eBars;
	 var plotter = options.plotter;
	 var currentGraphs = options.currentGraphs;
	 var graphs = options.graphs;
	 var srIDurlParam = options.srIDurlParam || '';
	$.ajax({
		url: url,
		async: false,
		type: 'GET',
		data: 'site_id=' + siteID + '&param_type=' + parentParam + '&ds_min=' + dischargeMin + '&ds_max=' + dischargeMax + calcTypeParamStr + srIDurlParam,
		context: this,
		complete: function(resp, status) {
			graphChildren.hide();
			if (status === 'success') {
				currentGraphs.push(parentParam);
				for (key in this._graphs) {
					var currentGraphExists = $.inArray(key, currentGraphs);
					try {
						if (currentGraphExists === -1) {
							graphDivE1(key).hide();
							this._graphs[key].destroy();
						}
						else {
							// do nothing
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
							graphDivE1(key).hide();
							this._graphs[key].destroy();
						}
						else {
							// do nothing
						}
					}
					catch(TypeError) {
						continue;
					}
				}
				var data = resp.responseText;
				var csvHeader = data.slice(0, data.indexOf('\n'));
				var csvHeaderLineBreak = csvHeader.replace(/(\r\n|\n|\r)/gm,"");
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
					//yRangePad: 20,
					strokePattern: [5, 5],
					highlightCircleSize: 4,
					drawPoints: true,
					pointSize: 3,
					customBars: eBars,
					plotter: plotter
				});
				if (columnCount < calc_type.length) {
					var missingDataArr = [];
					if (!searchForSubString('Eddy Total', headerArray) && $.inArray('eddy', calc_type) > -1) {
						missingDataArr.push('Eddy'); 
					}
					if (!searchForSubString('Channel Total', headerArray) && $.inArray('chan', calc_type) > -1) {
						missingDataArr.push('Channel'); 
					}
					if (!searchForSubString('Total Site', headerArray) && $.inArray('eddy_chan_sum', calc_type) > -1) {
						missingDataArr.push('Total Site'); 
					}
					var missingDataStr = missingDataArr.join(', ');
					var errorDisplay = '<p class="param-missing"> The following ' + displayName + ' parameters are unavailable for this site: ' + missingDataStr + '.</p>';
					graphDivEl(parentParam).append(errorDisplay);
					$('<br/>').insertAfter(graphDivEl(parentParam));
				}
				else {
					alert('Unable to retrieve data: ' + resp.status + ' : ' + resp.statusText);
				}
			}
		}
	});
	return graphs;
};