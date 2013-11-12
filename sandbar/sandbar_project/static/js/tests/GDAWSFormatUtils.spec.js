describe('Tests for GDAWSFormatUtils', function() {
	
	describe('Tests for GDAWSFormatUtils.getDygraphCSV', function() {
		it('Expects a properly formatted CSV for valid jsonResp', function() {
			var jsonResp = {success : {
				data : [{'time' : '2013-08-21T00:00:00','A1' : 1, 'A2' : 2},
				        {'time' : '2013-08-21T01:00:00', 'A1' : 2, 'A2' : 4},
				        {'time' : '2013-08-21T02:00:00', 'A1' : 3, 'A2' : 5}
				        ]
				}};
			var expectedResult = 'Time,A2Label\n' +
								 '2013-08-21T00:00:00,2\n' +
								 '2013-08-21T01:00:00,4\n' +
								 '2013-08-21T02:00:00,5\n';
			
			expect(SB.GDAWSFormatUtils.getDygraphCSV(jsonResp, 'A2', 'A2Label')).toEqual(expectedResult);
		});
		
		it('Expects a single label line if no data array in jsonResp', function() {
			var jsonResp = {success: {data : []}};
			expect(SB.GDAWSFormatUtils.getDygraphCSV(jsonResp, 'A2', 'A2Label')).toEqual('Time,A2Label\n');
		});
	});
	
	describe('GDAWSFormatUtils.getDataQueryString', function() {
		var result;
		
		beforeEach(function() {
			SB.Config = {
				SITE_PARAMETERS : {
					P1 : {
						param: 'parameter 1',
						colName: 'Param1'
					},
					P2 : {
						param: 'parameter 2',
						colName: 'Param2'
					},
					P3 : {
						param: 'parameter 3',
						colName: 'Param3'
					}
				}
			};
			
			result = SB.GDAWSFormatUtils.getDataQueryString('1357', '2013-04-01', '2013-04-04', ['P1', 'P3']);
		});
				
		it('Expects date range to be set correctly in returned string', function() {
			expect(result).toContain('beginPosition=2013-04-01');
			expect(result).toContain('endPosition=2013-04-04');
		});
		
		it('Expects params to be set correctly', function() {
			expect(result).toContain('column[]=inst!parameter 1!1357!Param1');
			expect(result).toContain('column[]=inst!parameter 3!1357!Param3');
			expect(result).not.toContain('Param2');
		});
	});
});