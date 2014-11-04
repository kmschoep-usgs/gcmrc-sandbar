SB.Config = {};
/*SB.Config.SITE_PARAMETERS = ['S Sand Cumul Load', 'Discharge']; */
SB.Config.SITE_PARAMETERS = {
	cumulSandLoad : {
		groupName : 'S Sand Cumul Load',
		colName : 'cumulLoad',
		description: {}, /* Filled in when page is loaded */
		site: null /* Filled in on page load */
	},
	discharge : {
		groupName : 'Discharge',
		colName: 'discharge',
		description: {}, /* Filled in when page is loaded */
		site: null /* Filled on on page load */
	}
};


