# Generated by Django 5.1.2 on 2024-10-23 10:47

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='antennatype',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='ratedvoltage',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='antennatype',
            name='type',
            field=models.CharField(help_text='Type of the antenna, e.g. Monopole, Dipole etc.', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='motor',
            name='stator_diameter',
            field=models.CharField(help_text='Two first digits of size (e.g. 28 from 2806)', max_length=2, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='motor',
            name='stator_height',
            field=models.CharField(help_text='Two last digits of size (e.g. 06 from 2806 or 06.5 from 2806.5)', max_length=4, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='motordetail',
            name='kv_per_volt',
            field=models.PositiveIntegerField(help_text='KV per volt', verbose_name='KV per volt'),
        ),
        migrations.AlterField(
            model_name='motordetail',
            name='max_power',
            field=models.PositiveIntegerField(help_text='Max power, W'),
        ),
        migrations.AlterField(
            model_name='motordetail',
            name='voltage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rated_voltage', to='components.ratedvoltage'),
        ),
    ]