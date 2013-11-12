SB.DateRange = function(startEl, endEl) {
	this.startEl = startEl;
	this.endEl = endEl;
	
	this.startEl.val(SB.Config.SITE_INITIAL_START_DATE).prop('min', SB.Config.SITE_MIN_DATE).prop('max', SB.Config.SITE_MAX_DATE);
	this.endEl.val(SB.Config.SITE_INITIAL_END_DATE).prop('min', SB.Config.SITE_MIN_DATE).prop('max', SB.Config.SITE_MAX_DATE);
	
	this.startEl.bind('blur', $.proxy(function() {
		var startVal = $(this.startEl).val();
		if (this.startEl.prop('max') >= startVal) {
			this.endEl.prop('min', startVal);
			return false;
		}
		
	}, this));
	
	this.endEl.bind('blur', $.proxy(function() {
		var endVal = $(this.endEl).val();
		if(this.endEl.prop('min') <= endVal) {
			this.startEl.prop('max', endVal);
			return false;
		}
	}, this));
	
};