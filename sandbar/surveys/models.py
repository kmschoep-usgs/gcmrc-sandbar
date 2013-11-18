
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
    eddy_size = models.DecimalField(max_digits=6, decimal_places=2)
    exp_ratio_8000 = models.DecimalField(max_digits=5, decimal_places=2)
    exp_ratio_45000 = models.DecimalField(max_digits=5, decimal_places=2)
    stage_change = models.DecimalField(max_digits=5, decimal_places=2)
    sed_budget_reach = models.CharField(max_length=100)
    campsite = models.CharField(max_length=3, choices=YES_NO)
    geom = models.PointField()
    
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
    calc_date = models.DateField()
    min_cfs =  models.IntegerField(max_length=6)
    max_cfs = models.IntegerField(max_length=6)
    area_amt = models.IntegerField(max_length=6)
    volume_amt = models.IntegerField(max_length=6)
    
    class Meta:
        db_table = 'area_volume_calc'
        unique_together = ('site', 'sandbar', 'calc_date')
        
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
    
        
