$(document).ready(function() {
	var map = L.map('sites-map-home', {
		center: [36.5, -112.4],
		zoom : 7,
		attributionControl: false,
		keyboard: false,
		zoomControl: false,
		scrollWheelZoom: false,
		doubleClickZoom: false,
		boxZoom: false
	});
	var geojsonURL = get_value('#geojson_sites');
	var geojsonLayer = L.geoJson.ajax(geojsonURL, {
		pointToLayer: function(feature, latlng) {
			return L.marker(latlng, {clickable: false});
		}
	});
	var baseLayer = L.tileLayer('http://services.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}.png')
	map.addLayer(baseLayer);
	map.addLayer(geojsonLayer);
});