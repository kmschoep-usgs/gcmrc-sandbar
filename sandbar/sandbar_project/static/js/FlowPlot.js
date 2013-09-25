function FlowPlot(divId /* String */) {
	this.graph = new Dygraph(divId, [], {});
};