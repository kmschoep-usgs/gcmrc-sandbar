function DateRange(startEl, endEl) {
	this.startEl = startEl;
	this.endEl = endEl;
	
	var startDate = '1996-01-01';
	var today = new Date().toISOString().slice(0, 10);
	
	this.startEl.val(startDate).prop('min', startDate).prop('max', today);
	this.endEl.val(today).prop('min', startDate).prop('max', today);
	
	this.startEl.bind('blur', $.proxy(function() {
		this.endEl.prop('min', $(this.startEl).val());
		return false;
	}, this));
	
	this.endEl.bind('blur', $.proxy(function() {
		this.startEl.prop('max', $(this.endEl).val());
	}, this));
	
};