timeSeriesGraph = new Dygraph (
		document.getElementById("timeseries-plot"),
		AREA_2D_URL,
		{
			xlabel: "Date",
			ylabel: "2D Area",
			showRangeSelector : true,
			yAxisLabelWidth: 95,
			labelsDivWidth: 300
		}
		);


timeSeriesGraph.resize(698, 320);