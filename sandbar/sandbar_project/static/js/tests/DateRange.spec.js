describe('Test SB.DateRange object', function() {
	
	var testDivEl;
	var dateRange;
	
	beforeEach(function() {
		var startHtml = '<input type="date" id="start-date" />';
		var endHtml = '<input type="date" id="end-date" />';
		$('body').append('<div id="test-div">' + startHtml + endHtml + '</div>');
		
		testDivEl = $('#test-div');
		
		spyOn(Date.prototype, 'toISOString').andReturn('2013-09-14T14:00:03.563Z');
		
		dateRange = new DateRange($('#start-date'), $('#end-date'));
	});
	
	afterEach(function() {
		testDivEl.remove();
	});
	
	it ('Expects the start date value is 1996-01-01 and end date is today', function() {
		expect(dateRange.startEl.val()).toEqual('1996-01-01');
		expect(dateRange.endEl.val()).toEqual('2013-09-14');
	});
	
	it('Expects the min and max props to be iniitally set to 1996-01-01 and today', function() {
		expect(dateRange.startEl.prop('min')).toEqual('1996-01-01');
		expect(dateRange.endEl.prop('min')).toEqual('1996-01-01');
		expect(dateRange.startEl.prop('max')).toEqual('2013-09-14');
		expect(dateRange.endEl.prop('max')).toEqual('2013-09-14')
	});
	it('Expects the min property on end date to update when start date changes', function() {
        dateRange.startEl.val('1900-01-01');
        dateRange.startEl.blur();
        
        expect(dateRange.endEl.prop('min')).toEqual('1900-01-01');
	});

	it('Expects the max property on start date to update when end date changes', function() {
        dateRange.endEl.val('1900-01-01');
        dateRange.endEl.blur();
        
        expect(dateRange.startEl.prop('max')).toEqual('1900-01-01');
	});

});