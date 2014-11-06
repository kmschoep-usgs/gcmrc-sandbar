$(document).ready(function() {
	$('#sites-table-div table').fixedHeaderTable({
		'height' : 400
	});
	
	var map = L.map('sites-map', {
		center: [36.5, -112.0],
		zoom : 7,
		attributionControl: false
	});
	
	var baseLayer = L.tileLayer('http://services.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}.png')
	map.addLayer(baseLayer);
	
	var siteMarkers =[];
	$('#sites-table tbody tr').each(function() {
		var siteNameLinkEl = $(this).find('.site-name-cell a');
		var thisMarker = new SiteMarker([$(this).data('geomY'), $(this).data('geomX')], {
			'title' : siteNameLinkEl.html(),
			'siteId' : $(this).data('siteId'),
			'url' : siteNameLinkEl.attr('href'),
			'riseOnHover' : true
		});
		thisMarker.on('click', function(e) {
			location.href = this.getUrl();
		});
		siteMarkers.push(thisMarker);
	});			
	L.layerGroup(siteMarkers).addTo(map);
});