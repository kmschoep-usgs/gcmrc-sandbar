from django.db import models
from django.conf import settings
from django.contrib.gis.db import models
#from django.contrib.gis.geos import GEOSGeometry, fromstr, fromfile,  Point

# Create your models here.

class Site(models.Model):
    YES_NO = (
        ('YES','Yes'),
        ('NO', 'No')
    )
    river_mile = models.DecimalField(max_digits=5, decimal_places=2)
    site_name = models.CharField(max_length=128)
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
    
class Survey(models.Model):
    site = models.ForeignKey(Site)
    survey_date = models.DateField()
    survey_method = models.CharField(max_length=100)
    class Meta:
        db_table = 'surveys'