SB.SitePlotMap = function(siteLat,siteLng) {
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
	var baseLayer = L.tileLayer('http://services.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}.png').addTo(map);
	var marker = L.marker([Number(siteLng), Number(siteLat)]).addTo(map);	
	map.setView([Number(siteLng), Number(siteLat)], 7);
	map.invalidateSize();
};