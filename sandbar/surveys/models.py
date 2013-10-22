
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
    gdaws_site_id = models.IntegerField(max_length=10, null=True)
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
        
