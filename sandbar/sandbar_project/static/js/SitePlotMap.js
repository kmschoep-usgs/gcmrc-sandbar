SB.SitePlotMap = function(siteId,siteLat,siteLng) {
	var map = L.map('site-loc-map-div', {
		center: [Number(siteLng), Number(siteLat)],
		zoom : 7,
		attributionControl: false,
		keyboard: false,
		zoomControl: false,
		scrollWheelZoom: false,
		doubleClickZoom: false,
		boxZoom: false
	});
	var geojsonURL = get_value('#geojson_sites');
	geojsonURL = geojsonURL + "?site_id=" + siteId;
	var geojsonLayer = L.geoJson.ajax(geojsonURL);
	var baseLayer = L.tileLayer('http://services.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}.png');
	map.addLayer(baseLayer);
	geojsonLayer.addTo(map);	
	
};