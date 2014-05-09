SB.TSPlots = function (graphsDivId /* id of div containing the divs for each parameter's graph */, siteId /* String */) {
	this.graphsDivEl = $('#' + graphsDivId);
	this._graphs = {}; // Holds current dygraphs
	this.siteId = siteId;
	
	//var graphId = function(key) {
	//	return key + '-graph-div';
	//}
	//var graphDivEl = function(key) {
	//	return $('#' + graphId(key));
	//};
	var graphDivEl = $('#timeseries-plot');
	// public object methods
	this.updatePlots = function(dischargeMin, dischargeMax /* String discharge inputs */) {
		
		this.graphsDivEl.children('#plots-loading-div').show();
		
		$.ajax({
			url: SB.AREA_2D_URL ,
			type: 'GET',
			data: 'site_id=' + siteId + '&ds_min=' + dischargeMin + '&ds_max=' + dischargeMax,
			context : this,
			complete : function(resp, status) {
				this.graphsDivEl.children('#plots-loading-div').hide();
				
				if (status === 'success') {					
					/* destroy previously created graphs */
						graphDivEl.hide();
						//this._graphs.destroy();
					// Update the selected graphs
					var graphs = {};
					var data = resp.responseText;
					graphDivEl.show();
					timeSeriesGraph = new Dygraph('timeseries-plot',
							data, {
						xlabel: "Date",
						ylabel: "2D Area",
						showRangeSelector : true,
						yAxisLabelWidth: 95,
						labelsDivWidth: 300,							
					});
					this._graphs = timeSeriesGraph;
				}
				else {
					alert('Unable to retrieve data: ' + resp.status + ' : ' + resp.statusText);
				}
			}
		});
	};
};