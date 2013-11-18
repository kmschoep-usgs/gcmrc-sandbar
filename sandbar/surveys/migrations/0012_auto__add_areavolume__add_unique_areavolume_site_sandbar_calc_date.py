# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AreaVolume'
        db.create_table('area_volume_calc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Site'])),
            ('sandbar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Sandbar'], null=True)),
            ('calc_date', self.gf('django.db.models.fields.DateField')()),
            ('min_cfs', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
            ('max_cfs', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
            ('area_amt', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
            ('volume_amt', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
        ))
        db.send_create_signal(u'surveys', ['AreaVolume'])

        # Adding unique constraint on 'AreaVolume', fields ['site', 'sandbar', 'calc_date']
        db.create_unique('area_volume_calc', ['site_id', 'sandbar_id', 'calc_date'])


    def backwards(self, orm):
        # Removing unique constraint on 'AreaVolume', fields ['site', 'sandbar', 'calc_date']
        db.delete_unique('area_volume_calc', ['site_id', 'sandbar_id', 'calc_date'])

        # Deleting model 'AreaVolume'
        db.delete_table('area_volume_calc')


    models = {
        u'surveys.areavolume': {
            'Meta': {'unique_together': "(('site', 'sandbar', 'calc_date'),)", 'object_name': 'AreaVolume', 'db_table': "'area_volume_calc'"},
            'area_amt': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'calc_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_cfs': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'min_cfs': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'sandbar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Sandbar']", 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Site']"}),
            'volume_amt': ('django.db.models.fields.IntegerField', [], {'max_length': '6'})
        },
        u'surveys.sandbar': {
            'Meta': {'unique_together': "(('site', 'sandbar_name'),)", 'object_name': 'Sandbar', 'db_table': "'site_sandbar_rel'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sandbar_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Site']"})
        },
        u'surveys.site': {
            'Meta': {'unique_together': "(('river_mile', 'site_name'),)", 'object_name': 'Site', 'db_table': "'sites'"},
            'campsite': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'deposit_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'eddy_size': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'exp_ratio_45000': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'exp_ratio_8000': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'gcmrc_site_id': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'gdaws_site_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'river_mile': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'river_side': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
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