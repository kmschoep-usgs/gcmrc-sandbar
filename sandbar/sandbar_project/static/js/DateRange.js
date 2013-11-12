SB.DateRange = function(startEl, endEl) {
	this.startEl = startEl;
	this.endEl = endEl;
	
	this.startEl.val(SB.Config.SITE_INITIAL_START_DATE).prop('min', SB.Config.SITE_MIN_DATE).prop('max', SB.Config.SITE_MAX_DATE);
	this.endEl.val(SB.Config.SITE_INITIAL_END_DATE).prop('min', SB.Config.SITE_MIN_DATE).prop('max', SB.Config.SITE_MAX_DATE);
	
	this.startEl.bind('blur', $.proxy(function() {
		if (this.startEl.get(0).checkValidity()) {
			this.endEl.prop('min', $(this.startEl).val());
			return false;
		}
		
	}, this));
	
	this.endEl.bind('blur', $.proxy(function() {
		if (this.endEl.get(0).checkValidity()) {
			this.startEl.prop('max', $(this.endEl).val());
			return false;
		}
	}, this));
	
};