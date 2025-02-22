# Generated by Django 5.1.5 on 2025-02-22 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('builds', '0001_initial'),
        ('components', '0001_initial'),
        ('documents', '0001_initial'),
        ('suggestions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='antennadocument',
            name='suggestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggested_documents', to='suggestions.antennasuggestion'),
        ),
        migrations.AddField(
            model_name='cameradocument',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='components.camera'),
        ),
        migrations.AddField(
            model_name='cameradocument',
            name='suggestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggested_documents', to='suggestions.camerasuggestion'),
        ),
        migrations.AddField(
            model_name='dronedocument',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='builds.drone'),
        ),
        migrations.AddField(
            model_name='flightcontrollerdocument',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='components.flightcontroller'),
        ),
        migrations.AddField(
            model_name='flightcontrollerdocument',
            name='suggestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggested_documents', to='suggestions.flightcontrollersuggestion'),
        ),
        migrations.AddField(
            model_name='framedocument',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='components.frame'),
        ),
        migrations.AddField(
            model_name='framedocument',
            name='suggestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggested_documents', to='suggestions.framesuggestion'),
        ),
        migrations.AddField(
            model_name='motordocument',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='components.motor'),
        ),
        migrations.AddField(
            model_name='motordocument',
            name='suggestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggested_documents', to='suggestions.motorsuggestion'),
        ),
        migrations.AddField(
            model_name='propellerdocument',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='components.propeller'),
        ),
        migrations.AddField(
            model_name='propellerdocument',
            name='suggestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggested_documents', to='suggestions.propellersuggestion'),
        ),
        migrations.AddField(
            model_name='receiverdocument',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='components.receiver'),
        ),
        migrations.AddField(
            model_name='receiverdocument',
            name='suggestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggested_documents', to='suggestions.receiversuggestion'),
        ),
        migrations.AddField(
            model_name='speedcontrollerdocument',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='components.speedcontroller'),
        ),
        migrations.AddField(
            model_name='speedcontrollerdocument',
            name='suggestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggested_documents', to='suggestions.speedcontrollersuggestion'),
        ),
        migrations.AddField(
            model_name='stackdocument',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='components.stack'),
        ),
        migrations.AddField(
            model_name='stackdocument',
            name='suggestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggested_documents', to='suggestions.stacksuggestion'),
        ),
        migrations.AddField(
            model_name='transmitterdocument',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='components.transmitter'),
        ),
        migrations.AddField(
            model_name='transmitterdocument',
            name='suggestion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggested_documents', to='suggestions.transmittersuggestion'),
        ),
    ]
