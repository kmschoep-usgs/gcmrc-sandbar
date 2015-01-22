SB.SitePlotMap = function(siteLat,siteLng) {
	var map;
	var latlng = L.latLng(parseFloat(siteLng), parseFloat(siteLat));
	map = L.map('site-loc-map-div', {
		center: latlng,
		zoom: 17,
		attributionControl: false
	});
	
	L.esri.dynamicMapLayer("http://arcweb.wr.usgs.gov/ArcGIS/rest/services/MapServiceImageryMay2009RGB/MapServer", {
		 opacity: 1
		 }).addTo(map); 
	//map.setView(latlng, 7);
	return map;
};