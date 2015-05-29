$(document).ready(function () {
	$('#content').imagesLoaded(function() {
		$('#content').isotope({
			itemSelector: '.item'
		});
	});
});
