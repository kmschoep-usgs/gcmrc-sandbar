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
	this.updatePlots = function(dischargeMin, dischargeMax /* String discharge inputs */, params, calc_type) {
		var calcTypeParamStr = '';
		for (i = 0; i < calc_type.length; i++) {
			calcTypeParamStr += '&calc_type=' + calc_type[i];
		}
		var showArea2d = $.inArray('area2d', params);
		if (showArea2d > -1) {
			this.graphsDivEl.children('#plots-loading-div').show();
			$.ajax({
				url: SB.AREA_2D_URL,
				type: 'GET',
				data: 'site_id=' + siteId + '&ds_min=' + dischargeMin + '&ds_max=' + dischargeMax + calcTypeParamStr,
				context : this,
				complete : function(resp, status) {
					this.graphsDivEl.children('#plots-loading-div').hide();
					
					if (status === 'success') {					
						/* destroy previously created graphs */
						for (key in this._graphs) {
							graphDivEl(key).hide();
							this._graphs[key].destroy();
						}
						// Update the selected graphs
						var graphs = {};
						for (var i = 0; i < params.length; i++) {
							var data = resp.responseText;
							graphDivEl(params[i]).show();
							graphs[params[i]] = new Dygraph(graphId(params[i]),
									data, {
								xlabel: "Date",
								ylabel: params[i],
								yAxisLabelWidth: 95,
								labelsDivWidth: 300,
								showRangeSelector: true,
								legend: 'always'
							});
						}
						this._graphs = graphs;
					}
					else {
						alert('Unable to retrieve data: ' + resp.status + ' : ' + resp.statusText);
					}
				}
			});
		}
	};
};