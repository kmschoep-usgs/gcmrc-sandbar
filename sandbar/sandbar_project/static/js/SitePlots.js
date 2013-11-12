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
	
	// public object methods
	this.updatePlots = function(startDate, endDate /* String dates */,
					 		    parameterNames /* array of parameter names to draw graphs, must match name in Config.SITE_PARAMETERS */) {
		
		this.graphsDivEl.children('#loading-div').show();
		
		$.ajax({
			url: SB.GDAWS_SERVICE + 'agg/',
			type: 'GET',
			data: SB.GDAWSFormatUtils.getDataQueryString(this.gdawsSiteId, startDate, endDate, parameterNames),
			context : this,
			complete : function(resp, status) {
				this.graphsDivEl.children('#loading-div').hide();

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
						var data = SB.GDAWSFormatUtils.getDygraphCSV($.parseJSON(resp.responseText), thisConfig.colName, thisConfig.shortLabel);
						graphDivEl(parameterNames[i]).show();
						
						graphs[parameterNames[i]] = new Dygraph(graphId(parameterNames[i]),
								data, {
							ylabel : thisConfig.graphYLabel,
							labelsDivWidth: 300,
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