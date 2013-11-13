SB.DateRange = function(startEl, endEl, initialStart, initialEnd, minDate, maxDate) {
	this.startEl = startEl;
	this.endEl = endEl;
	
	this.startEl.val(initialStart).attr('min', minDate).attr('max', maxDate);
	this.endEl.val(initialEnd).attr('min', minDate).attr('max', maxDate);
	
	this.startEl.bind('blur', $.proxy(function() {
		var startVal = $(this.startEl).val();
		// Don't update the attribute if the change is not valid
		// It would be easier to use checkValidity() but that's not available in IE9
		if (startVal >= this.startEl.attr('min') && startVal <= this.startEl.attr('max')) {
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