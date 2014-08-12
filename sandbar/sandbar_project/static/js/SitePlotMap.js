SB.SitePlotMap = function(siteLat,siteLng) {
	var map;
	var latlng = L.latLng(parseFloat(siteLng), parseFloat(siteLat));
	map = L.map('site-loc-map-div', {
		center: latlng,
		zoom: 17,
		attributionControl: false
	});
	
	var baseLayer = L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.png').addTo(map);
	var marker = L.marker(latlng).addTo(map);	
	//map.setView(latlng, 7);
	return map;
};