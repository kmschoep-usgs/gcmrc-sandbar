SB.SitePlotMap = function(siteLat,siteLng) {
	var map;
	var latlng = L.latLng(parseFloat(siteLng), parseFloat(siteLat));
	map = L.map('site-loc-map-div', {
		center: latlng,
		zoom: 7
	});
	
	var baseLayer = L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}.png').addTo(map);
	var marker = L.marker(latlng).addTo(map);	
	//map.setView(latlng, 7);
	return map;
};