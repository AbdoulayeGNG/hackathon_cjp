# Generated by Django 5.0.2 on 2025-05-14 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_report_options_report_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='location_lat',
            field=models.FloatField(verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='report',
            name='location_lng',
            field=models.FloatField(verbose_name='longitude'),
        ),
    ]
