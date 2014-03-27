# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AreaVolume.area_amt'
        db.delete_column('area_volume_calc', 'area_amt')

        # Deleting field 'AreaVolume.max_cfs'
        db.delete_column('area_volume_calc', 'max_cfs')

        # Deleting field 'AreaVolume.min_cfs'
        db.delete_column('area_volume_calc', 'min_cfs')

        # Adding field 'AreaVolume.calc_type'
        db.add_column('area_volume_calc', 'calc_type',
                      self.gf('django.db.models.fields.CharField')(max_length=15, null=True),
                      keep_default=False)

        # Adding field 'AreaVolume.plane_height'
        db.add_column('area_volume_calc', 'plane_height',
                      self.gf('django.db.models.fields.IntegerField')(max_length=6, null=True),
                      keep_default=False)

        # Adding field 'AreaVolume.area_2d_amt'
        db.add_column('area_volume_calc', 'area_2d_amt',
                      self.gf('django.db.models.fields.IntegerField')(max_length=6, null=True),
                      keep_default=False)

        # Adding field 'AreaVolume.area_3d_amt'
        db.add_column('area_volume_calc', 'area_3d_amt',
                      self.gf('django.db.models.fields.IntegerField')(max_length=6, null=True),
                      keep_default=False)


        # Changing field 'Survey.discharge'
        db.alter_column('surveys', 'discharge', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2))

    def backwards(self, orm):
        # Adding field 'AreaVolume.area_amt'
        db.add_column('area_volume_calc', 'area_amt',
                      self.gf('django.db.models.fields.IntegerField')(max_length=6, null=True),
                      keep_default=False)

        # Adding field 'AreaVolume.max_cfs'
        db.add_column('area_volume_calc', 'max_cfs',
                      self.gf('django.db.models.fields.IntegerField')(default=3, max_length=6),
                      keep_default=False)

        # Adding field 'AreaVolume.min_cfs'
        db.add_column('area_volume_calc', 'min_cfs',
                      self.gf('django.db.models.fields.IntegerField')(default=3, max_length=6),
                      keep_default=False)

        # Deleting field 'AreaVolume.calc_type'
        db.delete_column('area_volume_calc', 'calc_type')

        # Deleting field 'AreaVolume.plane_height'
        db.delete_column('area_volume_calc', 'plane_height')

        # Deleting field 'AreaVolume.area_2d_amt'
        db.delete_column('area_volume_calc', 'area_2d_amt')

        # Deleting field 'AreaVolume.area_3d_amt'
        db.delete_column('area_volume_calc', 'area_3d_amt')


        # Changing field 'Survey.discharge'
        db.alter_column('surveys', 'discharge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2))

    models = {
        u'surveys.areavolume': {
            'Meta': {'unique_together': "(('site', 'sandbar', 'calc_date'),)", 'object_name': 'AreaVolume', 'db_table': "'area_volume_calc'"},
            'area_2d_amt': ('django.db.models.fields.IntegerField', [], {'max_length': '6', 'null': 'True'}),
            'area_3d_amt': ('django.db.models.fields.IntegerField', [], {'max_length': '6', 'null': 'True'}),
            'calc_date': ('django.db.models.fields.DateField', [], {}),
            'calc_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plane_height': ('django.db.models.fields.IntegerField', [], {'max_length': '6', 'null': 'True'}),
            'sandbar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Sandbar']", 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Site']"}),
            'volume_amt': ('django.db.models.fields.IntegerField', [], {'max_length': '6', 'null': 'True'})
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
            'cur_stage_relation': ('django.db.models.fields.CharField', [], {'default': "'equation'", 'max_length': '100'}),
            'deposit_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'eddy_size': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'exp_ratio_45000': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'exp_ratio_8000': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'gcmrc_site_id': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'gdaws_site_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'river_mile': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'river_side': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'sed_budget_reach': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'stage_change': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'surveys.survey': {
            'Meta': {'object_name': 'Survey', 'db_table': "'surveys'"},
            'discharge': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Site']"}),
            'survey_date': ('django.db.models.fields.DateField', [], {}),
            'survey_method': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uncrt_a_8000': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'uncrt_b_8000': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['surveys']