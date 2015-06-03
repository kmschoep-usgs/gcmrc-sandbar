SB.Graphing = function() {
	var dealwithResponse = function(graphToMake, data, config, buildGraph) {
		var parseColData = function(str) {
			var result = null;
			var low = null, med = null, high = null;
			if (str) {
				var strSplit = str.split(';');
				if (2 < strSplit.length) {
					low = parseFloat(strSplit[0]);
					med = parseFloat(strSplit[1]);
					high = parseFloat(strSplit[2]);
				}
				else {
					med = parseFloat(str);
				}
			}
			if (!isNullUndefinedOrNaN(med)) {
				if (!isNullUndefinedOrNaN(low)) {
					low = med;
				}
				if (isNullUndefinedOrNaN(high)) {
					high = med;
				}
			}
			result = [low, med, high];
		}
	};
	return result;
};