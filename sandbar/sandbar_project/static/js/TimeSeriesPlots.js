function sandbarDataPlot(url, siteId, parentParam, dischargeMin, dischargeMax, calcTypeParamStr, parentParam, 
						 gcmrcPlots, currentGraphs, totalParams, yAxisLabel, eBars, plotter, srIDurlParam=null) {
	.ajax({
		url: url,
		async: false,
		type: 'GET',
		data: 'site_id=' + this.siteId + '&param_type=' + parentParam + '&ds_min=' + dischargeMin + '&ds_max=' + dischargeMax + calcTypeParamStr + srIDurlParam,
		context: this,
		complete: function(resp, status) {
			this.graphsDivE1.children('#plots-loading-div').hide();
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
				graphDivEl(parentParamSR).show();
				graphs[parentParam] = new Dygraph(graphId(parentParam)
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
				
			}
		}
	});
};