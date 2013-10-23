from django.db import models
from django.conf import settings

# Create your models here.
    
class Knight(models.Model):
    name = models.CharField(max_length=100)
    of_the_round_table = models.BooleanField()
    dances_whenever_able = models.BooleanField()
    new_column_name = models.CharField(max_length=5, blank=True)