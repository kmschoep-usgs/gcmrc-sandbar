# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sites'
        db.create_table('sites', (
            ('site_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('river_mile', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('deposit_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('eddy_size', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('exp_ratio_8000', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('exp_ratio_45000', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('stage_change', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('sed_budget_reach', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('campsite', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'surveys', ['Sites'])

        # Adding unique constraint on 'Sites', fields ['river_mile', 'site_name']
        db.create_unique('sites', ['river_mile', 'site_name'])

        # Adding model 'Surveys'
        db.create_table('surveys', (
            ('survey_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Sites'])),
            ('survey_date', self.gf('django.db.models.fields.DateField')()),
            ('survey_method', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'surveys', ['Surveys'])


    def backwards(self, orm):
        # Removing unique constraint on 'Sites', fields ['river_mile', 'site_name']
        db.delete_unique('sites', ['river_mile', 'site_name'])

        # Deleting model 'Sites'
        db.delete_table('sites')

        # Deleting model 'Surveys'
        db.delete_table('surveys')


    models = {
        u'surveys.sites': {
            'Meta': {'unique_together': "(('river_mile', 'site_name'),)", 'object_name': 'Sites', 'db_table': "'sites'"},
            'campsite': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'deposit_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'eddy_size': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'exp_ratio_45000': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'exp_ratio_8000': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'river_mile': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'sed_budget_reach': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'site_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'stage_change': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'surveys.surveys': {
            'Meta': {'object_name': 'Surveys', 'db_table': "'surveys'"},
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Sites']"}),
            'survey_date': ('django.db.models.fields.DateField', [], {}),
            'survey_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'survey_method': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['surveys']