SB.Config = {};
SB.Config.SITE_PARAMETERS = {
	cumulSandLoad : {
		param : 'Sand Cumul Load',
		colName : 'cumulLoad',
		graphYLabel : 'Cumulative Sand Load',
		shortLabel : 'Cumul Sand Load'
	},
	discharge : {
		param : 'Discharge',
		colName: 'discharge',
		graphYLabel : 'Discharge (cfs)',
		shortLabel : 'Discharge'
	}
};
SB.Config.SITE_INITIAL_END_DATE = new Date().toISOString().slice(0, 10);
SB.Config.SITE_INITIAL_START_DATE = new Date(new Date().getTime() - 30 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
SB.Config.SITE_MIN_DATE = '1996-01-01';
SB.Config.SITE_MAX_DATE = SB.Config.SITE_INITIAL_END_DATE;

