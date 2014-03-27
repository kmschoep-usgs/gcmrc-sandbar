# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AreaVolumeStg.calc_type'
        db.delete_column('area_volume_calc_stage', 'calc_type')

        # Deleting field 'AreaVolumeStg.site'
        db.delete_column('area_volume_calc_stage', 'site_id')

        # Deleting field 'AreaVolumeStg.sandbar_name'
        db.delete_column('area_volume_calc_stage', 'sandbar_name')

        # Deleting field 'AreaVolumeStg.calc_date'
        db.delete_column('area_volume_calc_stage', 'calc_date')

        # Adding field 'AreaVolumeStg.dataset'
        db.add_column('area_volume_calc_stage', 'dataset',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'AreaVolumeStg.calc_type'
        db.add_column('area_volume_calc_stage', 'calc_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True),
                      keep_default=False)

        # Adding field 'AreaVolumeStg.site'
        db.add_column('area_volume_calc_stage', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['surveys.Site']),
                      keep_default=False)

        # Adding field 'AreaVolumeStg.sandbar_name'
        db.add_column('area_volume_calc_stage', 'sandbar_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'AreaVolumeStg.calc_date'
        db.add_column('area_volume_calc_stage', 'calc_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 3, 13, 0, 0)),
                      keep_default=False)

        # Deleting field 'AreaVolumeStg.dataset'
        db.delete_column('area_volume_calc_stage', 'dataset')


    models = {
        u'surveys.areavolume': {
            'Meta': {'unique_together': "(('site', 'sandbar', 'calc_date', 'calc_type', 'plane_height'),)", 'object_name': 'AreaVolume', 'db_table': "'area_volume_calc'"},
            'area_2d_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'area_3d_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'calc_date': ('django.db.models.fields.DateField', [], {}),
            'calc_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plane_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'sandbar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Sandbar']", 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Site']"}),
            'volume_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'})
        },
        u'surveys.areavolumestg': {
            'Meta': {'object_name': 'AreaVolumeStg', 'db_table': "'area_volume_calc_stage'"},
            'area_2d_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'area_3d_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'dataset': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plane_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'volume_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'})
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