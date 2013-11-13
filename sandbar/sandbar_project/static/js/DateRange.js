SB.DateRange = function(startEl, endEl) {
	this.startEl = startEl;
	this.endEl = endEl;
	
	this.startEl.val(SB.Config.SITE_INITIAL_START_DATE).attr('min', SB.Config.SITE_MIN_DATE).attr('max', SB.Config.SITE_MAX_DATE);
	this.endEl.val(SB.Config.SITE_INITIAL_END_DATE).attr('min', SB.Config.SITE_MIN_DATE).attr('max', SB.Config.SITE_MAX_DATE);
	
	this.startEl.bind('blur', $.proxy(function() {
		var startVal = $(this.startEl).val();
		if (this.startEl.attr('max') >= startVal) {
			this.endEl.attr('min', startVal);
		}
		return false;
		
	}, this));
	
	this.endEl.bind('blur', $.proxy(function() {
		var endVal = $(this.endEl).val();
		if(this.endEl.attr('min') <= endVal) {
			this.startEl.attr('max', endVal);
		}
		return false;

	}, this));
	
};