SB.SitePageOnReady = function(gdawsSiteId) {
	
	var queryParams = 'site=' + gdawsSiteId;
	for (key in SB.Config.SITE_PARAMETERS) {
		queryParams += '&groupName=' + SB.Config.SITE_PARAMETERS[key].groupName;
	}
	
	// Fetch the parameter display information
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
				for (var i = 0; i < data.length; i++) {
					for (key in SB.Config.SITE_PARAMETERS) {
						if (SB.Config.SITE_PARAMETERS[key].groupName === data[i].groupName) {
							SB.Config.SITE_PARAMETERS[key].description = data[i];
							// Only really want date portion of time strings
							SB.Config.SITE_PARAMETERS[key].description.beginPosition = data[i].beginPosition.slice(0, 10);
							SB.Config.SITE_PARAMETERS[key].description.endPosition = data[i].endPosition.slice(0, 10);
							break;
						}
					}
				}
				
				// Create the parameter checkboxes
				var template = $('#param_template').html();
				for (key in SB.Config.SITE_PARAMETERS) {
					var data = {
						paramName : key, 
						description : SB.Config.SITE_PARAMETERS[key].description
					}
					$('#parameter-checkbox-div').append(Mustache.render(template, data));
				}
			}
			else {
				alert('Unable to contact plot web service: ' + resp.status + ' : ' + resp.statusText);
			}
			$('#page-loading-div').hide();
			$('#site-page-content').show();
		}
	});
	var dateRange = new SB.DateRange($('#start-date'), $('#end-date'), {});
				
	// Initialize dygraphs
	var sitePlots = new SB.SitePlots('graphs-div', gdawsSiteId);
	
	$('#update-plots-button').click(function(event) {
		if ($('form').valid()) {
			var params = [];
			$('#parameter-selection-div input:checked').each(function() {
				params.push($(this).val());
			});
			if (params.length === 0) {
				$('#parameter-errors').append('Please select one or more parameters to plot');
				$('#parameter-errors').show();
			}
			else {
				$('#parameter-errors').html('');
				$('#parameter-errors').hide();
				sitePlots.updatePlots(dateRange.startEl.val(), dateRange.endEl.val(), params);
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