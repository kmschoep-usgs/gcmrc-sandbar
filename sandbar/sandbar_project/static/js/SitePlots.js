SB.SitePlots = function (graphsDivId /* id of div containing the divs for each parameter's graph */, gdawsSiteId /* String */) {
	this.graphsDivEl = $('#' + graphsDivId);
	this._graphs = {}; // Holds current dygraphs
	this.gdawsSiteId = gdawsSiteId;
	
	var graphId = function(key) {
		return key + '-graph-div';
	}
	var graphDivEl = function(key) {
		return $('#' + graphId(key));
	};
	
	timeSeriesGraph = new Dygraph (
			document.getElementById("timeseries-plot"),
			AREA_2D_URL,
			{
				xlabel: "Date",
				ylabel: "2D Area",
				showRangeSelector : true
			}
			);
	
	// public object methods
	this.updatePlots = function(startDate, endDate /* String dates */,
					 		    parameterNames /* array of parameter names to draw graphs, must match name in Config.SITE_PARAMETERS */) {
		
		this.graphsDivEl.children('#graphs-loading-div').show();
		
		$.ajax({
			url: SB.GDAWS_SERVICE + 'agg/',
			type: 'GET',
			data: SB.GDAWSFormatUtils.getDataQueryString(this.gdawsSiteId, startDate, endDate, parameterNames),
			context : this,
			complete : function(resp, status) {
				this.graphsDivEl.children('#graphs-loading-div').hide();

				if (status === 'success') {					
					/* destroy previously created graphs */
					for (key in this._graphs) {
						graphDivEl(key).hide();
						this._graphs[key].destroy();
					}
					// Update the selected graphs
					var graphs = {};
					for (var i = 0; i < parameterNames.length; i++) {
						var thisConfig = SB.Config.SITE_PARAMETERS[parameterNames[i]];
						var data = SB.GDAWSFormatUtils.getDygraphCSV($.parseJSON(resp.responseText), thisConfig.colName, thisConfig.description.displayName);
						graphDivEl(parameterNames[i]).show();
						console.log(parameterNames[i]);
						graphs[parameterNames[i]] = new Dygraph(graphId(parameterNames[i]),
								data, {
							ylabel : thisConfig.description.displayName + ' (' + thisConfig.description.unitsShort + ')',
							labelsDivWidth: 300,
							yAxisLabelWidth: 95,
							showRangeSelector : true							
						});
					}
					this._graphs = graphs;
					
				}
				else {
					alert('Unable to retrieve data: ' + resp.status + ' : ' + resp.statusText);
				}
			}
		});
	};
};