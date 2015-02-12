describe('Test SiteMarker', function() {
	var thisSiteMarker = siteMarker([43.0, -110.0], {
		siteId: 1,
		url: '/fake/service/'
	});
	
	it ('Creates a marker with a siteId attribute', function() {
		expect(thisSiteMarker.getSiteId()).toBe(1);
	});
	
	it('Creates a marker with a url attribute', function() {
		expect(thisSiteMarker.getUrl()).toBe('/fake/service/');
	});
});