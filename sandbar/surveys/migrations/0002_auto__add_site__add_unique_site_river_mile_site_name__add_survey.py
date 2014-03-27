# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Site'
        db.create_table('sites', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('river_mile', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('deposit_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('eddy_size', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('exp_ratio_8000', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('exp_ratio_45000', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('stage_change', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('sed_budget_reach', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('campsite', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True, null=True)),
        ))
        db.send_create_signal(u'surveys', ['Site'])

        # Adding unique constraint on 'Site', fields ['river_mile', 'site_name']
        db.create_unique('sites', ['river_mile', 'site_name'])

        # Adding model 'Survey'
        db.create_table('surveys', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Site'])),
            ('survey_date', self.gf('django.db.models.fields.DateField')()),
            ('survey_method', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'surveys', ['Survey'])


    def backwards(self, orm):
        # Removing unique constraint on 'Site', fields ['river_mile', 'site_name']
        db.delete_unique('sites', ['river_mile', 'site_name'])

        # Deleting model 'Site'
        db.delete_table('sites')

        # Deleting model 'Survey'
        db.delete_table('surveys')


    models = {
        u'surveys.site': {
            'Meta': {'unique_together': "(('river_mile', 'site_name'),)", 'object_name': 'Site', 'db_table': "'sites'"},
            'campsite': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'deposit_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'eddy_size': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'exp_ratio_45000': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'exp_ratio_8000': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'river_mile': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'sed_budget_reach': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'stage_change': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'surveys.survey': {
            'Meta': {'object_name': 'Survey', 'db_table': "'surveys'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Site']"}),
            'survey_date': ('django.db.models.fields.DateField', [], {}),
            'survey_method': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['surveys']