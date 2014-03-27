
from django.contrib.gis.db import models
#from django.contrib.gis.geos import GEOSGeometry, fromstr, fromfile,  Point

# Create your models here.

class Site(models.Model):
    
    YES_NO = (
        ('YES','Yes'),
        ('NO', 'No')
    )
    river_mile = models.DecimalField(max_digits=5, decimal_places=2)
    river_side = models.CharField(max_length=1)
    site_name = models.CharField(max_length=128)
    gdaws_site_id = models.CharField(max_length=40, blank=True)
    gcmrc_site_id = models.CharField(max_length=5, blank=True)
    deposit_type = models.CharField(max_length=100)
    eddy_size = models.IntegerField(max_digits=6, null=True)
    exp_ratio_8000 = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    exp_ratio_45000 = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    stage_change = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    sed_budget_reach = models.CharField(max_length=100)
    cur_stage_relation = models.CharField(max_length=100, default="equation")
    campsite = models.CharField(max_length=3, choices=YES_NO)
    geom = models.PointField(blank=True, null=True)
    stage_discharge_coeff_a = models.DecimalField(max_digits= 16, decimal_places=13)
    stage_discharge_coeff_b = models.DecimalField(max_digits= 15, decimal_places=13)
    stage_discharge_coeff_c = models.DecimalField(max_digits= 15, decimal_places=15)
    
    class Meta:
        db_table = 'sites'
        unique_together = ('river_mile', 'site_name')
        
    objects = models.GeoManager()
    
    def __unicode__(self):
        return str(self.river_mile) + ' : ' + self.site_name
    
class Survey(models.Model):
    
    site = models.ForeignKey(Site)
    survey_date = models.DateField()
    survey_method = models.CharField(max_length=100)
    uncrt_a_8000 = models.IntegerField(max_length=3)
    uncrt_b_8000 = models.IntegerField(max_length=3)
    discharge = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        db_table = 'surveys'
        
    def __unicode__(self):
        return str(self.site) + ' on ' + str(self.survey_date)
    
class Sandbar(models.Model):
    
    site = models.ForeignKey(Site)
    sandbar_name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'site_sandbar_rel'
        unique_together = ('site', 'sandbar_name')
    
    def __unicode__(self):
        return str(self.sandbar_name) + ' on ' + str(self.site)

class AreaVolume(models.Model):
    site = models.ForeignKey(Site)
    sandbar = models.ForeignKey(Sandbar, null=True)
    calc_type = models.CharField(max_length=15, blank=True)
    calc_date = models.DateField()
    plane_height = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    area_2d_amt = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    area_3d_amt = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    volume_amt = models.DecimalField(max_digits=20, decimal_places=9, null=True)
    
    class Meta:
        db_table = 'area_volume_calc'
        unique_together = ('site', 'sandbar', 'calc_date', 'calc_type', 'plane_height')
        
    def __unicode__(self):
        return 'Site: ' + str(self.site) + '; Sandbar: ' + str(self.sandbar) + '; Date: ' + str(self.calc_date)
 
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
    
        
