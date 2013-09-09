SiteMarker = L.Marker.extend({
	options: {
		siteId : '',
		url: '',
	},

	getSiteId: function() {
		return this.options.siteId;
	},
	
	getUrl: function() {
		return this.options.url;
	}
});

siteMarker = function(latlng, options) {
	return new SiteMarker(latlng, options);
}