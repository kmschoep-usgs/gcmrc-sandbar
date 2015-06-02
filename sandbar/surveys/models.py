
from django.contrib.gis.db import models
#from django.contrib.gis.geos import GEOSGeometry, fromstr, fromfile,  Point

# Create your models here.

class Site(models.Model):
    
    YES_NO = (
        ('YES','Yes'),
        ('NO', 'No')
    )
    river_mile = models.FloatField()
    river_side = models.CharField(max_length=1)
    site_name = models.CharField(max_length=128)
    gdaws_site_id = models.CharField(max_length=40, blank=True)
    gcmrc_site_id = models.CharField(max_length=5, blank=True)
    deposit_type = models.CharField(max_length=100)
    eddy_size = models.IntegerField(null=True)
    exp_ratio_8000 = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    exp_ratio_45000 = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    stage_change = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    sed_budget_reach = models.CharField(max_length=100)
    cur_stage_relation = models.CharField(max_length=200, default="equation")
    campsite = models.CharField(max_length=3, choices=YES_NO)
    geom = models.PointField(blank=True, null=True)
    stage_discharge_coeff_a = models.DecimalField(max_digits= 16, decimal_places=13)
    stage_discharge_coeff_b = models.DecimalField(max_digits= 15, decimal_places=13)
    stage_discharge_coeff_c = models.DecimalField(max_digits= 18, decimal_places=15)
    photo_from = models.CharField(max_length=10, blank=True)
    photo_view = models.CharField(max_length=30, blank=True)
    flow_direction = models.CharField(max_length=30, blank=True)
    image_name = models.CharField(max_length=50, blank=True)
    image_name_med = models.CharField(max_length=50, blank=True)
    image_name_small = models.CharField(max_length=50, blank=True)
    p_month = models.CharField(max_length=20, blank=True)
    p_day = models.CharField(max_length=2, blank=True)
    p_year = models.CharField(max_length=4, blank=True)
    gdaws_site_display = models.CharField(max_length=100, blank=True)
    secondary_gdaws_site_id = models.CharField(max_length=40, blank=True)
    second_gdaws_site_disp = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'sites'
        unique_together = ('river_mile', 'site_name')
        
    objects = models.GeoManager()
    
    def __unicode__(self):
        return str(self.river_mile) + ' : ' + self.site_name
    
    def elevationM(self, dis):
        '''
        Equation:
        Z=a+b*ds-c*ds^2
        where,
        Z = elevation, in meters
        ds is discharge in cfs

        inputs:
        ds = user input
        a = sites.STAGE_DISCHARGE_COEFF_A
        b = sites.STAGE_DISCHARGE_COEFF_B
        c = sites.STAGE_DISCHARGE_COEFF_C

        The resulting Z-range is compared to area_volume_calc.plane_height.
        '''
        #result = []
        result = float(self.stage_discharge_coeff_a)+float(self.stage_discharge_coeff_b)*dis-float(self.stage_discharge_coeff_c)*pow(dis,2)
        #result_max = float(self.stage_discharge_coeff_a)+float(self.stage_discharge_coeff_b)*ds_max-float(self.stage_discharge_coeff_c)*pow(ds_max,2)
        
        #result.append(str(result_min))
        #result.append(str(result_max))
        return result
    
    
class Survey(models.Model):
    
    site = models.ForeignKey(Site)
    survey_date = models.DateField()
    survey_method = models.CharField(max_length=100)
    uncrt_a_8000 = models.IntegerField()
    uncrt_b_8000 = models.IntegerField()
    discharge = models.DecimalField(max_digits=8, decimal_places=2)
    trip_date = models.DateField(null=True)
    calc_type = models.CharField(max_length=20, blank=True)
    sandbar_id = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'surveys'
        
    def __unicode__(self):
        return str(self.site) + '-' + str(self.sandbar_id) + ' on ' + str(self.survey_date) + ' for ' + str(self.calc_type) + ' at ' + str(self.discharge)
    
    
class Sandbar(models.Model):
    
    site = models.ForeignKey(Site)
    sandbar_name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'site_sandbar_rel'
        unique_together = ('site', 'sandbar_name')
    
    def __unicode__(self):
        return str(self.sandbar_name) + ' on ' + str(self.site)
    
    def _get_river_mile(self):
        
        river_mile = float(self.site.river_mile)
        return river_mile
    river_mile = property(_get_river_mile)
      
    def _get_river_side(self):
        
        river_side = str(self.site.river_side)
        return river_side
    river_side = property(_get_river_side)
    
    def _get_site_name(self):
        
        site_name = self.site.site_name
        return site_name
    site_name = property(_get_site_name)
    

class AreaVolume(models.Model):
    site = models.ForeignKey(Site)
    sandbar = models.ForeignKey(Sandbar, null=True)
    calc_type = models.CharField(max_length=15, blank=True)
    calc_date = models.DateField()
    plane_height = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    area_2d_amt = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    area_3d_amt = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    volume_amt = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    prev_plane_height = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    next_plane_height = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    
    class Meta:
        db_table = 'area_volume_calc'
        unique_together = ('site', 'sandbar', 'calc_date', 'calc_type', 'plane_height','prev_plane_height','next_plane_height')
        
    def __unicode__(self):
        return 'Site: ' + str(self.site) + '; Sandbar: ' + str(self.sandbar) + '; Date: ' + str(self.calc_date) + '; Plane Height:' + str(self.plane_height)
    
 
class AreaVolumeStg(models.Model):
    dataset = models.CharField(max_length=100, blank=True)
    plane_height =  models.CharField(max_length=100, blank=True)
    area_2d_amt = models.CharField(max_length=100, blank=True)
    area_3d_amt = models.CharField(max_length=100, blank=True)
    volume_amt = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'area_volume_calc_stage'
        
    def __unicode__(self):
        return 'Site: ' + str(self.site) + '; Sandbar: ' + str(self.sandbar) + '; Date: ' + str(self.calc_date)
       
#class SiteStar(models.Model):
#    site_id = models.IntegerField(max_length=12, primary_key=True)
#    short_name = models.CharField(max_length=32)
#    location_geopoint = models.PointField()
    
#    class Meta:
#        db_table = 'site_star'
        
#    objects = models.GeoManager()
        
#    def __unicode__(self):
#        return str(self.site_id)

class AreaVolumeOutput(models.Model):
    site_id = models.FloatField()
    calc_date = models.DateField()
    min_elev = models.FloatField()
    max_elev = models.FloatField()
    eddy_int_area = models.FloatField()
    eddy_s_int_area = models.FloatField()
    eddy_r_int_area = models.FloatField()
    sum_reatt_sep_area = models.FloatField()
    eddy_int_volume = models.FloatField()
    eddy_s_int_volume = models.FloatField()
    eddy_r_int_volume = models.FloatField()
    sum_reatt_sep_vol = models.FloatField()
    eddy_vol_error_low = models.FloatField()
    eddy_s_vol_error_low = models.FloatField()
    eddy_r_vol_error_low = models.FloatField()
    sum_reatt_sep_vel = models.FloatField()
    eddy_vol_error_high = models.FloatField()
    eddy_s_vol_error_high = models.FloatField()
    eddy_r_vol_error_high = models.FloatField()
    sum_reatt_sep_veh = models.FloatField()
    dy_chan_int_vol = models.CharField(max_length=100, blank=True)
    dy_eddy_int_vol = models.CharField(max_length=100, blank=True)
    dy_eddy_s_vol = models.CharField(max_length=100, blank=True)
    dy_eddy_r_vol = models.CharField(max_length=100, blank=True)
    dy_eddy_sum_vol = models.CharField(max_length=100, blank=True)
    dy_ts_int_vol = models.CharField(max_length=100, blank=True)    
    chan_int_area = models.FloatField()
    chan_int_volume = models.FloatField()
    chan_vol_error_low = models.FloatField()
    chan_vol_error_high = models.FloatField()
    ts_int_area = models.FloatField()
    ts_int_volume = models.FloatField()
    ts_vol_error_low = models.FloatField()
    ts_vol_error_high = models.FloatField()
    
    class Meta:
        managed = False
