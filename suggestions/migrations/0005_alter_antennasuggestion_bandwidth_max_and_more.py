# Generated by Django 5.1.3 on 2025-01-18 22:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0001_initial'),
        ('suggestions', '0004_alter_antennasuggestion_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antennasuggestion',
            name='bandwidth_max',
            field=models.FloatField(blank=True, help_text='Max. bandwidth (frequency) of the antenna', null=True),
        ),
        migrations.AlterField(
            model_name='antennasuggestion',
            name='bandwidth_min',
            field=models.FloatField(blank=True, help_text='Min. bandwidth (frequency) of the antenna', null=True),
        ),
        migrations.AlterField(
            model_name='antennasuggestion',
            name='center_frequency',
            field=models.FloatField(blank=True, help_text='Center frequency of the antenna', null=True),
        ),
        migrations.AlterField(
            model_name='antennasuggestion',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='components.antennatype'),
        ),
    ]
