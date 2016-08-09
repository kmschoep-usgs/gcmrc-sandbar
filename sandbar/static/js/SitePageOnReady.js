SB.SitePageOnReady = function(gdawsSiteId, dischargeSite, siteId) {
	var dateRange;
	var srIDs;
	var queryParams = 'site=' + gdawsSiteId + '&site=' + dischargeSite;
	var internalSiteId = siteId;
	SB.Config.SITE_PARAMETERS.discharge.site = dischargeSite;
	SB.Config.SITE_PARAMETERS.cumulSandLoad.site = gdawsSiteId;
	for (key in SB.Config.SITE_PARAMETERS) {
		queryParams += '&groupName=' + SB.Config.SITE_PARAMETERS[key].groupName;
	}
	var gcmrcStartDate;
	var gcmrcEndDate;
	
	var sandbarStartDate;
	var sandbarEndDate;
	
	//set default discharges
	$('#ds-min').val(8000);
	$('#ds-max').val(60000);
	//Set Plot title
	$('#panel-title').html('Sandbar Metrics Between Stage Elevations Associated with Discharges of ' + $('#ds-min').val() + ' and ' + $('#ds-max').val() + ' cfs (ft<sup>3</sup>/s)');
	// Fetch the parameter display information from GCMRC
	$.ajax({
		url: SB.GDAWS_SERVICE + 'service/param/json/param/', 
		type: 'GET',
		async: false,
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
							if (SB.Config.SITE_PARAMETERS[key].groupName === data[i].groupName && SB.Config.SITE_PARAMETERS[key].site === data[i].site) {
								SB.Config.SITE_PARAMETERS[key].description = data[i];
								// Only really want date portion of time strings
								SB.Config.SITE_PARAMETERS[key].description.beginPosition = data[i].beginPosition.slice(0, 10);
								SB.Config.SITE_PARAMETERS[key].description.endPosition = data[i].endPosition.slice(0, 10);
								SB.Config.SITE_PARAMETERS[key].description.siteName = data[i].SiteDisplayName;

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
					gcmrcStartDate = minDateText;
					gcmrcEndDate = maxDateText;
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
		async: false,
		data: 'site_id=' + internalSiteId,
		dataType: 'json',
		complete: function(resp, status) {
			var template = $('#app_param_template').html();
			var respJSON = $.parseJSON(resp.responseText);
			var area2dParam = respJSON.paramNames.area2d;
			var volumeParam = respJSON.paramNames.volume;
			var startDate = respJSON.calcDates.min;
			var endDate = respJSON.calcDates.max;
			var siteSrIDs = respJSON.sandbarIDs;
			if (startDate === null && endDate === null) {
				$('#no-data-warning').append('No sandbar data is available for this site.');
				$('#no-data-warning').show();
			}
			var appCheckBoxParam = {
					wrapperParam: [
					               {areaParamVal: 'area2d', areaParam: area2dParam, minDate: startDate, maxDate:endDate},
					               {areaParamVal: 'volume', areaParam: volumeParam, minDate: startDate, maxDate:endDate}
					               ],
					wrapperSubParam: [
							          {subParamValue: 'eddy', subParamLabel: 'Eddy', subParamTitle: 'Eddy'},
							          {subParamValue: 'chan', subParamLabel: 'Channel', subParamTitle: 'Channel area and/or volume can only be plotted for discharges less than 8000 cfs.'},
							          {subParamValue: 'eddy_chan_sum', subParamLabel: 'Total Site', subParamTitle: 'Total Site area and/or volume can only be plotted for discharges less than 8000 cfs.'}
							          ]
			};
			$('#sb-parameter-checkbox-div').append(Mustache.render(template, appCheckBoxParam));
			$('div.sub-param-group input:checkbox').attr('disabled', true);
			sandbarStartDate = startDate;
			sandbarEndDate = endDate;
			srIDs = siteSrIDs;
		}
	});
	
	// Initialize dygraphs
	var tsPlots = new SB.TSPlots('sandbar-plots', siteId);
	var sitePlots = new SB.SitePlots('gcmrc-plots', gdawsSiteId, dischargeSite);
	

	$('#sep-reatt').click(function(event) {
		var checkboxIdArr = [];
		$('#parameter-selection-div input[name="sb-param"]:checked').each(function() {
			var checkboxIdVal = $(this).val();
			var checkboxIdChan = checkboxIdVal + '-chan-checkbox';
			var checkboxIdTotalSite = checkboxIdVal + '-eddy_chan_sum-checkbox';
			checkboxIdArr.push(checkboxIdChan);
			checkboxIdArr.push(checkboxIdTotalSite);
		});
		if ($('#sep-reatt').is(':checked') || parseFloat($('#ds-min').val()) >= 8000) {
			disableChanTotalSite();
		}
		else {
			for (i = 0; i < checkboxIdArr.length; i++) {
				var checkboxID = checkboxIdArr[i];
				enableChanTotalSite(checkboxID);
			}
		}	
	});

	$('#ds-min').change(function(event) {
		var checkedStatusSBParam = $('input[name="sb-param"]').is(':checked');
		var checkboxIdArr = []
		$('#parameter-selection-div input[name="sb-param"]:checked').each(function() {
			var checkboxIdVal = $(this).val();
			var checkboxIdChan = checkboxIdVal + '-chan-checkbox';
			var checkboxIdTotalSite = checkboxIdVal + '-eddy_chan_sum-checkbox';
			checkboxIdArr.push(checkboxIdChan);
			checkboxIdArr.push(checkboxIdTotalSite);
		});
		if (parseFloat($('#ds-min').val()) < 8000 && checkedStatusSBParam) {
			for (i = 0; i < checkboxIdArr.length; i++) {
				var checkboxID = checkboxIdArr[i];
				enableChanTotalSite(checkboxID);
			}
		}
		else {
			disableChanTotalSite();
		}
	});

	$('#update-plots-button, #download-data').click(function(event) {
		var clickTrigger = $(this).attr('id');
		if ($('form').valid()) {
			var gcmrcParams = [];
			var sandbarParams = [];
			var subParam = [];
			var srParam = {srPlot: false, srIDs: null};
			var errorExists = 0;
			$('#parameter-selection-div input[type=checkbox]:checked').each(function() {
				var parentClass = $(this).parent().attr('class');
				if ($(this).val() != 'area2d' && $(this).val() != 'volume' && parentClass != 'sub-param-group' && $(this).attr('id') != 'sep-reatt') {
					gcmrcParams.push($(this).val());
				}
				else if ($(this).attr('id') === 'sep-reatt') {
					srParam.srPlot = true;
					srParam.srIDs = srIDs;
				}
				else if ($(this).attr('name') === 'sb-param') {
					if (srParam.srPlot === true) {
						var separationParam = $(this).val() + '-sr-sep';
						var reattachmentParam = $(this).val() + '-sr-reatt';
						sandbarParams.push(separationParam);
						sandbarParams.push(reattachmentParam);
					}
					else {
						sandbarParams.push($(this).val());
					}
				}
				else if ($(this).attr('name') === 'sb-subparam') {
					var parentID = $(this).parent().attr('id');
					var selectParentStr = '#' + parentID;
					var parentSibling = $(selectParentStr).siblings('input[name="sb-param"]')
					var parentSiblingCheckboxVal = parentSibling.val();
					var parentSiblingLabelText = $(selectParentStr).siblings('label').text()
					
					if (parentSiblingCheckboxVal === 'area2d') {
						var paramUnit = 'm' + '2'.sup();
						var displayName = 'Area';
					}
					else if (parentSiblingCheckboxVal === 'volume') {
						var paramUnit = 'm' + '3'.sup();
						var displayName = 'Volume';
					}
					else {
						paramUnit = 'Unit Not Specified';
					}
					var parentFound = false;
					for (var i = 0; i < subParam.length; i++) {
						var paramValStr = subParam[i].paramVal;
						if (paramValStr === parentSiblingCheckboxVal) {
							subParam[i].subParamVals.push($(this).val()); 
							parentFound = true;
						}
					}
					if (parentFound === false) {
						var mapping = {paramVal: parentSiblingCheckboxVal, 
									   displayName: displayName,
									   paramUnit: paramUnit,
									   subParamVals: [$(this).val()]}
						subParam.push(mapping);
					}
				}
				else {
					//do nothing
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
			
			var sandbarParamsLength = sandbarParams.length;
			var sandbarSubParamsLength = subParam.length;
			if (sandbarParamsLength >= 1 && sandbarSubParamsLength === 0) {
				errorExists = 1;
				$('#parameter-errors').append('A subparameter must be selected for Area plots.');
			}
			
			if ($('#sep-reatt').is(':checked')) {
				if ($('#ds-min').val() != '' && Number($('#ds-min').val()) < 8000) {
					if (errorExists === 0) {
						$('#parameter-errors').html('');
					}
					else {
						$('#parameter-errors').append('<br>');
					}
					errorExists = 1;
					$('#parameter-errors').append('Minimum Discharge must be greater than or equal to 8000 cfs to plot separation/reattachment bars separately.');
				}
			}
			
			if (Number($('#ds-min').val()) > Number($('#ds-max').val())) {
				if (errorExists === 0) {
					$('#parameter-errors').html('');
				}
				else {
					$('#parameter-errors').append('<br>');
				}
				errorExists = 1;
				$('#parameter-errors').append('Maximum Discharge must be greater than or equal to minimum discharge.');
			}
			if (isNaN(Number($('#ds-min').val())) || isNaN(Number($('#ds-max').val()))) {
				if (errorExists === 0) {
					$('#parameter-errors').html('');
				}
				else {
					$('#parameter-errors').append('<br>');
				}
				errorExists = 1;
				$('#parameter-errors').append('Discharge values must be numeric.');
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
			if (Number($('#ds-min').val()) > 0 && Number($('#ds-min').val()) < 5000) {
				if (errorExists === 0) {
					$('#parameter-errors').html('');
				}
				else {
					$('#parameter-errors').append('<br>');
				}
				errorExists = 1;
				$('#parameter-errors').append('The stage-discharge relationship for discharge below 5000 cfs is invalid. To plot sandbar area and volume below 5000 cfs, please enter 0 for Discharge for Lower Bound.');
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
			}
			if (errorExists === 0 && clickTrigger != "download-data") {
				$('#parameter-errors').html('');
				$('#parameter-errors').hide();
				var plotStartDate = createPlotDates(sandbarStartDate, gcmrcStartDate);
				var plotEndDate = createPlotDates(sandbarEndDate, gcmrcEndDate);
				$('#panel-title').html('Sandbar Metrics Between Stage Elevations Associated with Discharges of ' + $('#ds-min').val() + ' and ' + $('#ds-max').val() + ' cfs (ft<sup>3</sup>/s)');
				sitePlots.updatePlots(plotStartDate, plotEndDate, gcmrcParams, tsPlots._graphs, params, sandbarStartDate);
				tsPlots.updatePlots($('#ds-min').val(), $('#ds-max').val(), subParam, sitePlots._graphs, params, srParam);
				
				var blockRedraw = false;
				$(document).ajaxStop(function() {
					var combinedGraphs = collect(sitePlots._graphs, tsPlots._graphs);
					for (key in combinedGraphs) {
						combinedGraphs[key].updateOptions({
							drawCallback: function(me, initial) {
								if (blockRedraw || initial) return;
								blockRedraw = true;
								var range = me.xAxisRange();
								for (keyname in combinedGraphs) {
									if (combinedGraphs[keyname] == me) continue;
									combinedGraphs[keyname].updateOptions({
										dateWindow: range
									});
								}
								blockRedraw = false;
							}
						});
					}					
				});
			}
			else if (errorExists === 0 && clickTrigger === "download-data") {
				$('#parameter-errors').html('');
				$('#parameter-errors').hide();
				var downloadURL = createLink(siteId, $('#ds-min').val(), $('#ds-max').val(), subParam);
				$('a#download-data').attr("href", downloadURL);
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
