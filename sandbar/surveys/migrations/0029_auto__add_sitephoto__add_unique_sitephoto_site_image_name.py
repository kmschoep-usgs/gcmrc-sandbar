# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SitePhoto'
        db.create_table('site_photos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['surveys.Site'])),
            ('photo_from', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('photo_view', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('flow_direction', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('image_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('image_name_med', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('image_name_small', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'surveys', ['SitePhoto'])

        # Adding unique constraint on 'SitePhoto', fields ['site', 'image_name']
        db.create_unique('site_photos', ['site_id', 'image_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'SitePhoto', fields ['site', 'image_name']
        db.delete_unique('site_photos', ['site_id', 'image_name'])

        # Deleting model 'SitePhoto'
        db.delete_table('site_photos')


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
            'gcmrc_site_id': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'gdaws_site_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'river_mile': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'river_side': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'sed_budget_reach': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'stage_change': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'stage_discharge_coeff_a': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '13'}),
            'stage_discharge_coeff_b': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '13'}),
            'stage_discharge_coeff_c': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '15'})
        },
        u'surveys.sitephoto': {
            'Meta': {'unique_together': "(('site', 'image_name'),)", 'object_name': 'SitePhoto', 'db_table': "'site_photos'"},
            'flow_direction': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'image_name_med': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'image_name_small': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'photo_from': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'photo_view': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['surveys.Site']"})
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