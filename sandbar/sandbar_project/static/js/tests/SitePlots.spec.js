describe('Test SitePlots', function() {
	
	beforeEach(function() {
		var html = '<div id="graphs-div">' + 
			'<div id="graphs-loading-div"></div>' +
			'<div id="P1-graph-div" style="display:none;"></div>' + 
			'<div id="P2-graph-div" style="display:none;"></div>' +
			'<div id="P3-graph-div" style="display:none;"></div>' + 
			'</div>';
		$('body').append(html);
		
		SB.Config = {
			SITE_PARAMETERS : {
				P1 : {
					param: 'parameter 1',
					colName: 'Param1',
					description: {
						displayName: 'P1 data',
						unitsShort : 'm'
					}
				},
				P2 : {
					param: 'parameter 2',
					colName: 'Param2',
					description: {
						displayName: 'P2 data',
						unitsShort : 'km'
					}
				},
				P3 : {
					param: 'parameter 3',
					colName: 'Param3',
					description: {
						displayName: 'P3 data',
						unitsShort : 'mi'
					}
				}
			}
		};
	});
	
	afterEach(function() {
		$('#graphs-div').remove();
	});
	
	it('Should  define attributes on object creation', function() {
		
		var sitePlots = new SB.SitePlots('graphs-div', '1357');
		expect(sitePlots.graphsDivEl).not.toBeNull();
		expect(sitePlots.gdawsSiteId).toEqual('1357');
	});
	
	describe('Test method updatePlots', function() {
		
		var sitePlots;
		var tsPlots._graphs
		var xhr;
		var requests;
		
		beforeEach(function() {
			sitePlots = new SB.SitePlots('graphs-div', '1367');
			tsPlots._graphs = {area6d: 'blah'}
			SB.GDAWS_SERVICE = 'http://fakegdaws/service/';
			
			xhr = sinon.useFakeXMLHttpRequest();
            requests = [];
            xhr.onCreate = function(req) {
                    requests.push(req);
            };
		});
		
		afterEach(function() {
			xhr.restore();
		});
		
		it('Expects loading div to be visible before ajax call completes', function() {
			sitePlots.updatePlots('2013-04-01', '2013-04-04', ['P2', 'P3'], tsPlots._graphs, ['P2', 'P3', 'P4', 'P5']);
			expect($('#graphs-loading-div').is(':visible')).toBe(undefined);
		});
		
		it('Expects ajax to be called', function() {
			sitePlots.updatePlots('2013-04-01', '2013-04-04', ['P2', 'P3'], tsPlots._graphs, ['P2', 'P3', 'P4', 'P5']);
			
			expect(requests.length).toBe(1);
			expect(requests[0].url).toContain('http://fakegdaws/service/agg');
			expect(requests[0].url).toContain(SB.GDAWSFormatUtils.getDataQueryString('1367', '2468', '2013-04-01', '2013-04-04', ['P2', 'P3']));
		});
		
		describe('Successful ajax call', function() {
			beforeEach(function() {
				var csvData = 'Time,A2Label\n' +
					'2013-08-21T00:00:00,2\n' +
					'2013-08-21T01:00:00,4\n' +
					'2013-08-21T02:00:00,5\n';
			
				sitePlots.updatePlots('2013-04-01', '2013-04-04', ['P2', 'P3'], tsPlots._graphs, ['P2', 'P3', 'P4', 'P5']);
			
				spyOn(SB.GDAWSFormatUtils, 'getDygraphCSV').andReturn(csvData);
			
				requests[0].respond(200, {'Content-Type' : 'application/json'}, '{"output": "data"}');
			});
		
			it('Expects successful ajax request to parse the results', function() {			
				expect(SB.GDAWSFormatUtils.getDygraphCSV.calls.length).toEqual(2);
			});
			
			it('Expects the selected Dygraphs to be created',function() {
				expect(sitePlots._graphs['P1']).not.toBeDefined();
				expect(sitePlots._graphs['P2']).toBeDefined();
				expect(sitePlots._graphs['P3']).toBeDefined();
			});
			
			it('expects the selected graph divs to be visible and the loading div to be hidden', function() {				
				expect($('#P1-graph-div').is(':visible')).toBe(false);
				expect($('#P2-graph-div').is(':visible')).toBe(true);
				expect($('#P3-graph-div').is(':visible')).toBe(true);
				
				expect($('#loading-div').is(':visible')).toBe(false);
			});
		});
			
		it('Expects ajax request failure to show alert and loading-div to be hidden', function() {
			sitePlots.updatePlots('2013-04-01', '2013-04-04', ['P2', 'P3'], tsPlots._graphs, ['P2', 'P3', 'P4', 'P5']);
			spyOn(window, 'alert');
			requests[0].respond(500, '', '');
			expect(window.alert).toHaveBeenCalled();
			expect($('#loading-div').is(':visible')).toBe(false);
		});
		
	});
	
});
