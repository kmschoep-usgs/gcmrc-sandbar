SiteMarker = L.Marker.extend({
	options: {
		siteId : ''
	},

	getSiteId: function() {
		return this.options.siteId;
	}
});

siteMarker = function(latlng, options) {
	return new SiteMarker(latlng, options);
}