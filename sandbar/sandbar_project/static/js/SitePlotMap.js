SB.SitePlotMap = function(siteLat,siteLng) {
	var map;
	var latlng = L.latLng(parseFloat(siteLng), parseFloat(siteLat));
	map = L.map('site-loc-map-div', {
		center: latlng,
		zoom: 18,
		attributionControl: false
	});
	
	//var baseLayer = L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.png').addTo(map);
	L.esri.dynamicMapLayer("https://grandcanyon.usgs.gov/arcgis/rest/services/Imagery/IMG_GC_2013_05_4BAND_8B_EARTHDATA/ImageServer", {
		 opacity: 1
	 }).addTo(map); 
	var marker = L.marker(latlng).addTo(map);
	//map.setView(latlng, 7);
	return map;
};