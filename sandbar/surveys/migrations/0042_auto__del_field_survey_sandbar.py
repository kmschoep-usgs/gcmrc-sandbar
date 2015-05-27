# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Survey.sandbar'
        db.delete_column('surveys', 'sandbar')


    def backwards(self, orm):
        # Adding field 'Survey.sandbar'
        db.add_column('surveys', 'sandbar',
                      self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True),
                      keep_default=False)


    models = {
        u'surveys.areavolume': {
            'Meta': {'unique_together': "(('site', 'sandbar', 'calc_date', 'calc_type', 'plane_height', 'prev_plane_height', 'next_plane_height'),)", 'object_name': 'AreaVolume', 'db_table': "'area_volume_calc'"},
            'area_2d_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'area_3d_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'calc_date': ('django.db.models.fields.DateField', [], {}),
            'calc_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_plane_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'plane_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'prev_plane_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'}),
            'sandbar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Sandbar']", 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Site']"}),
            'volume_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '9'})
        },
        u'surveys.areavolumeoutput': {
            'Meta': {'object_name': 'AreaVolumeOutput', 'managed': 'False'},
            'calc_date': ('django.db.models.fields.DateField', [], {}),
            'chan_int_area': ('django.db.models.fields.FloatField', [], {}),
            'chan_int_volume': ('django.db.models.fields.FloatField', [], {}),
            'chan_vol_error_high': ('django.db.models.fields.FloatField', [], {}),
            'chan_vol_error_low': ('django.db.models.fields.FloatField', [], {}),
            'dy_chan_int_vol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dy_eddy_int_vol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dy_eddy_r_vol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dy_eddy_s_vol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dy_eddy_sum_vol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dy_ts_int_vol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'eddy_int_area': ('django.db.models.fields.FloatField', [], {}),
            'eddy_int_volume': ('django.db.models.fields.FloatField', [], {}),
            'eddy_r_int_area': ('django.db.models.fields.FloatField', [], {}),
            'eddy_r_int_volume': ('django.db.models.fields.FloatField', [], {}),
            'eddy_r_vol_error_high': ('django.db.models.fields.FloatField', [], {}),
            'eddy_r_vol_error_low': ('django.db.models.fields.FloatField', [], {}),
            'eddy_s_int_area': ('django.db.models.fields.FloatField', [], {}),
            'eddy_s_int_volume': ('django.db.models.fields.FloatField', [], {}),
            'eddy_s_vol_error_high': ('django.db.models.fields.FloatField', [], {}),
            'eddy_s_vol_error_low': ('django.db.models.fields.FloatField', [], {}),
            'eddy_vol_error_high': ('django.db.models.fields.FloatField', [], {}),
            'eddy_vol_error_low': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_elev': ('django.db.models.fields.FloatField', [], {}),
            'min_elev': ('django.db.models.fields.FloatField', [], {}),
            'site_id': ('django.db.models.fields.FloatField', [], {}),
            'sum_reatt_sep_area': ('django.db.models.fields.FloatField', [], {}),
            'sum_reatt_sep_veh': ('django.db.models.fields.FloatField', [], {}),
            'sum_reatt_sep_vel': ('django.db.models.fields.FloatField', [], {}),
            'sum_reatt_sep_vol': ('django.db.models.fields.FloatField', [], {}),
            'ts_int_area': ('django.db.models.fields.FloatField', [], {}),
            'ts_int_volume': ('django.db.models.fields.FloatField', [], {}),
            'ts_vol_error_high': ('django.db.models.fields.FloatField', [], {}),
            'ts_vol_error_low': ('django.db.models.fields.FloatField', [], {})
        },
        u'surveys.areavolumestg': {
            'Meta': {'object_name': 'AreaVolumeStg', 'db_table': "'area_volume_calc_stage'"},
            'area_2d_amt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'area_3d_amt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plane_height': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'volume_amt': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
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
            'cur_stage_relation': ('django.db.models.fields.CharField', [], {'default': "'equation'", 'max_length': '200'}),
            'deposit_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'eddy_size': ('django.db.models.fields.IntegerField', [], {'max_length': '6', 'null': 'True'}),
            'exp_ratio_45000': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'exp_ratio_8000': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'flow_direction': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gcmrc_site_id': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'gdaws_site_display': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'gdaws_site_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'image_name_med': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'image_name_small': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'p_day': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'p_month': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'p_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'photo_from': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'photo_view': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'river_mile': ('django.db.models.fields.FloatField', [], {}),
            'river_side': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'second_gdaws_site_disp': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'secondary_gdaws_site_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'sed_budget_reach': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'stage_change': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'stage_discharge_coeff_a': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '13'}),
            'stage_discharge_coeff_b': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '13'}),
            'stage_discharge_coeff_c': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '15'})
        },
        u'surveys.survey': {
            'Meta': {'object_name': 'Survey', 'db_table': "'surveys'"},
            'discharge': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Site']"}),
            'survey_date': ('django.db.models.fields.DateField', [], {}),
            'survey_method': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trip_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'uncrt_a_8000': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'uncrt_b_8000': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['surveys']