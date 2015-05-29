# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AreaVolumeOutput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_id', models.FloatField()),
                ('calc_date', models.DateField()),
                ('min_elev', models.FloatField()),
                ('max_elev', models.FloatField()),
                ('eddy_int_area', models.FloatField()),
                ('eddy_s_int_area', models.FloatField()),
                ('eddy_r_int_area', models.FloatField()),
                ('sum_reatt_sep_area', models.FloatField()),
                ('eddy_int_volume', models.FloatField()),
                ('eddy_s_int_volume', models.FloatField()),
                ('eddy_r_int_volume', models.FloatField()),
                ('sum_reatt_sep_vol', models.FloatField()),
                ('eddy_vol_error_low', models.FloatField()),
                ('eddy_s_vol_error_low', models.FloatField()),
                ('eddy_r_vol_error_low', models.FloatField()),
                ('sum_reatt_sep_vel', models.FloatField()),
                ('eddy_vol_error_high', models.FloatField()),
                ('eddy_s_vol_error_high', models.FloatField()),
                ('eddy_r_vol_error_high', models.FloatField()),
                ('sum_reatt_sep_veh', models.FloatField()),
                ('dy_chan_int_vol', models.CharField(max_length=100, blank=True)),
                ('dy_eddy_int_vol', models.CharField(max_length=100, blank=True)),
                ('dy_eddy_s_vol', models.CharField(max_length=100, blank=True)),
                ('dy_eddy_r_vol', models.CharField(max_length=100, blank=True)),
                ('dy_eddy_sum_vol', models.CharField(max_length=100, blank=True)),
                ('dy_ts_int_vol', models.CharField(max_length=100, blank=True)),
                ('chan_int_area', models.FloatField()),
                ('chan_int_volume', models.FloatField()),
                ('chan_vol_error_low', models.FloatField()),
                ('chan_vol_error_high', models.FloatField()),
                ('ts_int_area', models.FloatField()),
                ('ts_int_volume', models.FloatField()),
                ('ts_vol_error_low', models.FloatField()),
                ('ts_vol_error_high', models.FloatField()),
            ],
            options={
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AreaVolume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calc_type', models.CharField(max_length=15, blank=True)),
                ('calc_date', models.DateField()),
                ('plane_height', models.DecimalField(null=True, max_digits=20, decimal_places=9)),
                ('area_2d_amt', models.DecimalField(null=True, max_digits=20, decimal_places=9)),
                ('area_3d_amt', models.DecimalField(null=True, max_digits=20, decimal_places=9)),
                ('volume_amt', models.DecimalField(null=True, max_digits=20, decimal_places=9)),
                ('prev_plane_height', models.DecimalField(null=True, max_digits=20, decimal_places=9)),
                ('next_plane_height', models.DecimalField(null=True, max_digits=20, decimal_places=9)),
            ],
            options={
                'db_table': 'area_volume_calc',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AreaVolumeStg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dataset', models.CharField(max_length=100, blank=True)),
                ('plane_height', models.CharField(max_length=100, blank=True)),
                ('area_2d_amt', models.CharField(max_length=100, blank=True)),
                ('area_3d_amt', models.CharField(max_length=100, blank=True)),
                ('volume_amt', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'db_table': 'area_volume_calc_stage',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sandbar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sandbar_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'site_sandbar_rel',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('river_mile', models.FloatField()),
                ('river_side', models.CharField(max_length=1)),
                ('site_name', models.CharField(max_length=128)),
                ('gdaws_site_id', models.CharField(max_length=40, blank=True)),
                ('gcmrc_site_id', models.CharField(max_length=5, blank=True)),
                ('deposit_type', models.CharField(max_length=100)),
                ('eddy_size', models.IntegerField(max_length=6, null=True)),
                ('exp_ratio_8000', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('exp_ratio_45000', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('stage_change', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('sed_budget_reach', models.CharField(max_length=100)),
                ('cur_stage_relation', models.CharField(default=b'equation', max_length=200)),
                ('campsite', models.CharField(max_length=3, choices=[(b'YES', b'Yes'), (b'NO', b'No')])),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('stage_discharge_coeff_a', models.DecimalField(max_digits=16, decimal_places=13)),
                ('stage_discharge_coeff_b', models.DecimalField(max_digits=15, decimal_places=13)),
                ('stage_discharge_coeff_c', models.DecimalField(max_digits=18, decimal_places=15)),
                ('photo_from', models.CharField(max_length=10, blank=True)),
                ('photo_view', models.CharField(max_length=30, blank=True)),
                ('flow_direction', models.CharField(max_length=30, blank=True)),
                ('image_name', models.CharField(max_length=50, blank=True)),
                ('image_name_med', models.CharField(max_length=50, blank=True)),
                ('image_name_small', models.CharField(max_length=50, blank=True)),
                ('p_month', models.CharField(max_length=20, blank=True)),
                ('p_day', models.CharField(max_length=2, blank=True)),
                ('p_year', models.CharField(max_length=4, blank=True)),
                ('gdaws_site_display', models.CharField(max_length=100, blank=True)),
                ('secondary_gdaws_site_id', models.CharField(max_length=40, blank=True)),
                ('second_gdaws_site_disp', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'db_table': 'sites',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('survey_date', models.DateField()),
                ('survey_method', models.CharField(max_length=100)),
                ('uncrt_a_8000', models.IntegerField(max_length=3)),
                ('uncrt_b_8000', models.IntegerField(max_length=3)),
                ('discharge', models.DecimalField(max_digits=8, decimal_places=2)),
                ('trip_date', models.DateField(null=True)),
                ('calc_type', models.CharField(max_length=20, blank=True)),
                ('sandbar_id', models.IntegerField(null=True)),
                ('site', models.ForeignKey(to='surveys.Site')),
            ],
            options={
                'db_table': 'surveys',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='site',
            unique_together=set([('river_mile', 'site_name')]),
        ),
        migrations.AddField(
            model_name='sandbar',
            name='site',
            field=models.ForeignKey(to='surveys.Site'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='sandbar',
            unique_together=set([('site', 'sandbar_name')]),
        ),
        migrations.AddField(
            model_name='areavolume',
            name='sandbar',
            field=models.ForeignKey(to='surveys.Sandbar', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='areavolume',
            name='site',
            field=models.ForeignKey(to='surveys.Site'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='areavolume',
            unique_together=set([('site', 'sandbar', 'calc_date', 'calc_type', 'plane_height', 'prev_plane_height', 'next_plane_height')]),
        ),
    ]
