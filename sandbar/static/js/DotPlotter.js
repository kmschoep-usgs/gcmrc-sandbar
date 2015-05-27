SB.DotPlotter = function(e) {
	var g = e.dygraph;
	var setName = e.setName;
	var strokeWidth = e.strokeWidth;

	var borderWidth = g.getOption("strokeBorderWidth", setName);
	var drawPointCallback = g.getOption("drawPointCallback", setName) ||
			Dygraph.Circles.DEFAULT;
	var strokePattern = g.getOption("strokePattern", setName);
	var drawPoints = g.getOption("drawPoints", setName);
	var pointSize = g.getOption("pointSize", setName);

	var color = e.color;
	var fillAlpha = g.getOption('fillAlpha', setName);
	var rgb = new RGBColorParser(color);
	var err_color =
			'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',' + fillAlpha + ')';

	var points = e.points;
	var iter = Dygraph.createIterator(points, 0, points.length,
			DygraphCanvasRenderer._getIteratorPredicate(
			g.getOption("connectSeparatedPoints")));

	var area = e.plotArea;
	var ctx = e.drawingContext;

	var convertToCanvasY = function(y, areaH, areaY) {
		return areaH * y + areaY;
	};
	
	var isNullUndefinedOrNaN = function(x) {
		return (x === null ||
				x === undefined ||
				isNaN(x));
	};
	var prevPoint = null;
	while (iter.hasNext) {
		var point = iter.next();
		if (!isNullUndefinedOrNaN(point.canvasy)) {
			if (!isNullUndefinedOrNaN(point.y_top) && !isNullUndefinedOrNaN(point.y_bottom)
					&& point.y_top !== point.y_bottom) {
				var topY = convertToCanvasY(point.y_top, area.h, area.y);
				var bottomY = convertToCanvasY(point.y_bottom, area.h, area.y);
				
				//Draw Line
				ctx.strokeStyle = 'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',1)';
				ctx.lineWidth = 2;
				ctx.beginPath();
				ctx.moveTo(point.canvasx, topY);
				ctx.lineTo(point.canvasx, bottomY);
				ctx.closePath();
				ctx.stroke();

				ctx.beginPath();
				ctx.moveTo(point.canvasx - pointSize, bottomY);
				ctx.lineTo(point.canvasx + pointSize, bottomY);
				ctx.closePath();
				ctx.stroke();

				ctx.beginPath();
				ctx.moveTo(point.canvasx - pointSize, topY);
				ctx.lineTo(point.canvasx + pointSize, topY);
				ctx.closePath();
				ctx.stroke();

			}

			//Add Point
			drawPointCallback(g, setName, ctx, point.canvasx, point.canvasy, color, pointSize);
		}
	}
};