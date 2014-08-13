SB.DateRange = function(startEl, endEl, options /* Object */) {
	/*
	 * The following options are used
	 * initialStart - date string to set startEl's value. If not specified but initialEnd is this will be one month before
	 * initialEnd - date string to set endEl's value
	 * minDate - dateString to set min prop
	 * maxDate - dateString to set max prop
	 */
	var today = new Date();
	
	this._options = {
		initialStart : new Date(today.getTime() - 30 * 24 * 60 *60 *1000).toISOString().slice(0, 10),
		initialEnd : today.toISOString().slice(0, 10),
		minDate : '1900-01-01',
		maxDate : today.toISOString().slice(0, 10)
	}

	this.startEl = startEl;
	this.endEl = endEl;
	$.extend(this._options, options);
	if (('initialEnd' in options) && (!('initialStart' in options))) {
		var initialEndDate = new Date(this._options.initialEnd);
		this._options.initialStart = new Date((new Date(this._options.initialEnd)).getTime() - 30 * 24 * 60 * 60 *1000).toISOString().slice(0,10);
	}
	
	this.startEl.val(this._options.initialStart).attr('min', this._options.minDate).attr('max', this._options.initialEnd);
	this.endEl.val(this._options.initialEnd).attr('min', this._options.initialStart).attr('max', this._options.maxDate);
	
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