describe('Test SB.DateRange object', function() {
	
	var testDivEl;
	var dateRange;
	
	beforeEach(function() {
		var startHtml = '<input type="date" id="start-date" />';
		var endHtml = '<input type="date" id="end-date" />';
		$('body').append('<div id="test-div">' + startHtml + endHtml + '</div>');
		
		testDivEl = $('#test-div');
		
		dateRange = new SB.DateRange($('#start-date'), $('#end-date'), {
			initialEnd : '2013-09-14',
			minDate: '1996-01-01',
			maxDate: '2013-09-14'
		});
	});
	
	afterEach(function() {
		testDivEl.remove();
	});
	
	it ('Expects the start date value and end date value to be initialized', function() {
		expect(dateRange.startEl.val()).toEqual('2013-08-15');
		expect(dateRange.endEl.val()).toEqual('2013-09-14');
	});
	
	it('Expects the min and max props to be set', function() {
		expect(dateRange.startEl.prop('min')).toEqual('1996-01-01');
		expect(dateRange.endEl.prop('min')).toEqual('2013-08-15');
		expect(dateRange.startEl.prop('max')).toEqual('2013-09-14');
		expect(dateRange.endEl.prop('max')).toEqual('2013-09-14')
	});
	it('Expects the min property on end date to update when start date changes', function() {
        dateRange.startEl.val('1997-01-01');
        dateRange.startEl.blur();
        
        expect(dateRange.endEl.prop('min')).toEqual('1997-01-01');
	});

	it('Expects the max property on start date to update when end date changes', function() {
        dateRange.endEl.val('1998-01-01');
        dateRange.endEl.blur();
        
        expect(dateRange.startEl.prop('max')).toEqual('2013-09-14');
	});
	
	it('Expects the min property on end date to be unchanged if the start date entered value is not valid', function() {
		dateRange.startEl.val('2013-10-14');
		dateRange.startEl.blur();		
		expect(dateRange.endEl.prop('min')).toEqual('2013-08-15');
		
		dateRange.startEl.val('1995-01-01');
		dateRange.startEl.blur();
		expect(dateRange.endEl.prop('min')).toEqual('2013-08-15');
	});
	
	it('Expects the max property on start date to be unchanged if the end date entered is not valid', function() {
		dateRange.endEl.val('1995-01-01');
		dateRange.endEl.blur();		
		expect(dateRange.startEl.prop('max')).toEqual('2013-09-14');
		
		dateRange.endEl.val('2013-10-14');
		dateRange.endEl.blur90;
		expect(dateRange.startEl.prop('max')).toEqual('2013-09-14');
	});

});