SB.SitePageOnReady = function(gdawsSiteId, siteId) {
	var dateRange;
	var queryParams = 'site=' + gdawsSiteId;
	var internalSiteId = siteId;
	for (key in SB.Config.SITE_PARAMETERS) {
		queryParams += '&groupName=' + SB.Config.SITE_PARAMETERS[key].groupName;
	}
	
	// Fetch the parameter display information from GCMRC
	$.ajax({
		url: SB.GDAWS_SERVICE + 'service/param/json/param/', 
		type: 'GET',
		data: queryParams,
		dataType: 'json',
		complete: function(resp, status) {
			if (status === 'success') {
				// Parse response and put into SB.Config.SITE_PARAMETERS
				var respJSON = $.parseJSON(resp.responseText);
				var data = respJSON.success.data
				if (data) {
					var minDate;
					var maxDate;

					var template = $('#param_template').html();

					for (var i = 0; i < data.length; i++) {
						for (key in SB.Config.SITE_PARAMETERS) {
							if (SB.Config.SITE_PARAMETERS[key].groupName === data[i].groupName) {
								SB.Config.SITE_PARAMETERS[key].description = data[i];
								// Only really want date portion of time strings
								SB.Config.SITE_PARAMETERS[key].description.beginPosition = data[i].beginPosition.slice(0, 10);
								SB.Config.SITE_PARAMETERS[key].description.endPosition = data[i].endPosition.slice(0, 10);

								// Create the parameters's checkbox
								var checkboxData = {
									paramName : key, 
									description : SB.Config.SITE_PARAMETERS[key].description
								}
								$('#parameter-checkbox-div').append(Mustache.render(template, checkboxData));
								
								// Update minDate and maxDate
								var beginDate = new Date(data[i].beginPosition);
								var endDate = new Date(data[i].endPosition);
								if ((!minDate) || (minDate > beginDate)) {
									minDate = beginDate
								}
								if ((!maxDate) || (maxDate < endDate)) {
									maxDate = endDate;
								}
								break;
							}
						}
					}
				
					// Update the dateRange limits and set initial Dates.
					minDateText = minDate.toISOString().slice(0,10);
					maxDateText = maxDate.toISOString().slice(0,10);
					
					dateRange = new SB.DateRange($('#start-date'), $('#end-date'), {
						initialEnd : maxDateText,
						minDate: minDateText,
						maxDate: maxDateText
					});
					
					$('#parameter-checkbox-div').prop('disabled', false);
				}
				else {
					$('#update-plots-button').prop('disabled', true);
					$('#parameter-checkbox-div').append('<span class="text-danger">No data is available for the default GDAWS site, ' + gdawsSiteId + '</span>');
				}
			}
			else {
				$('#update-plots-button').prop('disabled', true);
				$('#parameter-checkbox-div').append('<span class="text-danger">Unable to contact plot web service: ' + resp.status + ' : ' + resp.statusText);
			}
			$('#page-loading-div').hide();
			$('#site-page-content').show();
		}
	});
	
	$.ajax({
		url: SB.SITE_AREA_CALC_URL,
		type: 'GET',
		data: 'site_id=' + internalSiteId,
		dataType: 'json',
		complete: function(resp, status) {
			var template = $('#app_param_template').html();
			var respJSON = $.parseJSON(resp.responseText);
			var area2dParam = respJSON.paramNames.area2d;
			var startDate = respJSON.calcDates.min;
			var endDate = respJSON.calcDates.max;
			var appCheckBoxParam = {
				areaParam: area2dParam,
				minDate: startDate,
				maxDate: endDate
			};
			$('#parameter-checkbox-div').append(Mustache.render(template, appCheckBoxParam));
		}
	});
	
	
	
	// Initialize dygraphs
	var sitePlots = new SB.SitePlots('graphs-div', gdawsSiteId);
	var tsPlots = new SB.TSPlots('graphs-div', siteId);
	
	$('#update-plots-button').click(function(event) {
		if ($('form').valid()) {
			var gcmrcParams = [];
			var sandbarParams = [];
			var errorExists = 0;
			$('#parameter-selection-div input:checked').each(function() {
				if ($(this).val() != 'Area 2D') {
					gcmrcParams.push($(this).val());
				}
				else {
					sandbarParams.push($(this).val());
				}
			});
			var params = gcmrcParams.concat(sandbarParams);
			if (params.length === 0) {
				if (errorExists === 0) {
					$('#parameter-errors').html('');
				} 
				else {
					$('#parameter-errors').append('<br>');
				}
				errorExists = 1;
				$('#parameter-errors').append('Please select one or more parameters to plot.');
			}
			if (Number($('#ds-min').val()) > Number($('#ds-max').val())) {
				if (errorExists === 0) {
					$('#parameter-errors').html('');
				}
				else {
					$('#parameter-errors').append('<br>');
				}
				errorExists = 1;
				$('#parameter-errors').append('Maximum Discharge must be greater or equal to minimum discharge.');
			}
			if ($('#ds-min').val() === '') {
				if (errorExists === 0) {
					$('#parameter-errors').html('');
				}
				else {
					$('#parameter-errors').append('<br>');
				}
				errorExists = 1;
				$('#parameter-errors').append('Please enter a value for minimum discharge.');
				//$('#parameter-errors').show();
			}
			if ($('#ds-max').val() === '') {
				if (errorExists === 0) {
					$('#parameter-errors').html('');
				}
				else {
					$('#parameter-errors').append('<br>');
				}
				errorExists = 1;
				$('#parameter-errors').append('Please enter a value for maximum discharge.');
				//$('#parameter-errors').show();
			}
			if (errorExists === 0) {
				$('#parameter-errors').html('');
				$('#parameter-errors').hide();
				sitePlots.updatePlots(dateRange.startEl.val(), dateRange.endEl.val(), gcmrcParams);
				tsPlots.updatePlots( $('#ds-min').val(), $('#ds-max').val(), dateRange.startEl.val(), dateRange.endEl.val(), params);
				}
			else {
				$('#parameter-errors').show();
			}
		}
	});
	$('form').validate({
		onsubmit: false,
		errorClass: 'text-danger',
		errorPlacement: function(error, element) {
			error.appendTo(element.parent());
		},
		
	});
};