console.log(AREA_2D_URL);

timeseriesGraph = new Dygraph (
							document.getElementById("timeseries-plot"),
							AREA_2D_URL,
							{
								xlabel: "Date",
								ylabel: "2D Area"
							}
							)