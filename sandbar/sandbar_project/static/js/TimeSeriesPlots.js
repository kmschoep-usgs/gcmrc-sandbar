
timeSeriesGraph = new Dygraph (
		document.getElementById("timeseries-plot"),
		AREA_2D_URL + '&ds_min=' + $('#ds-min').val() + '&ds_max=' + $('#ds-max').val() ,
		{
			xlabel: "Date",
			ylabel: "2D Area",
			showRangeSelector : true,
			yAxisLabelWidth: 95,
			labelsDivWidth: 300,
			axes: {
				x: {
					ticker: function(a, b, pixels, opts, dygraph, vals) {
						var chosen = Dygraph.pickDateTickGranularity(a, b, pixels, opts);
						if (chosen >= 0) {
							var axisTicks = Dygraph.getDateAxis(a, b, chosen, opts, dygraph);
							return axisTicks;
						}
						else {
							return [];
						}
					}
				}
			}
		}
		);


timeSeriesGraph.resize(698, 320);