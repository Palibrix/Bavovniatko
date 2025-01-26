# Generated by Django 5.1.5 on 2025-01-26 16:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('components', '0001_initial'),
        ('suggestions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='antennaconnectorsuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='antennasuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.antenna'),
        ),
        migrations.AddField(
            model_name='antennasuggestion',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='components.antennatype'),
        ),
        migrations.AddField(
            model_name='antennasuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='antennatypesuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.antennatype'),
        ),
        migrations.AddField(
            model_name='antennatypesuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='camerasuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.camera'),
        ),
        migrations.AddField(
            model_name='camerasuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='camerasuggestion',
            name='video_formats',
            field=models.ManyToManyField(to='components.videoformat'),
        ),
        migrations.AddField(
            model_name='existingantennadetailsuggestion',
            name='antenna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='components.antenna', verbose_name='Antenna'),
        ),
        migrations.AddField(
            model_name='existingantennadetailsuggestion',
            name='connector_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='components.antennaconnector'),
        ),
        migrations.AddField(
            model_name='existingantennadetailsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='components.antennadetail'),
        ),
        migrations.AddField(
            model_name='existingantennadetailsuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='existingcameradetailsuggestion',
            name='camera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='components.camera', verbose_name='Camera'),
        ),
        migrations.AddField(
            model_name='existingcameradetailsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='components.cameradetail'),
        ),
        migrations.AddField(
            model_name='existingcameradetailsuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='existingframecameradetailsuggestion',
            name='frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_camera_details', to='components.frame', verbose_name='Frame'),
        ),
        migrations.AddField(
            model_name='existingframecameradetailsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='components.framecameradetail'),
        ),
        migrations.AddField(
            model_name='existingframecameradetailsuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='existingframemotordetailsuggestion',
            name='frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_motor_details', to='components.frame', verbose_name='Frame'),
        ),
        migrations.AddField(
            model_name='existingframemotordetailsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='components.framemotordetail'),
        ),
        migrations.AddField(
            model_name='existingframemotordetailsuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='existingframevtxdetailsuggestion',
            name='frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_vtx_details', to='components.frame', verbose_name='Frame'),
        ),
        migrations.AddField(
            model_name='existingframevtxdetailsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='components.framevtxdetail'),
        ),
        migrations.AddField(
            model_name='existingframevtxdetailsuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='framesuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.frame'),
        ),
        migrations.AddField(
            model_name='framesuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='suggestedantennadetailsuggestion',
            name='connector_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='components.antennaconnector'),
        ),
        migrations.AddField(
            model_name='suggestedantennadetailsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.antennadetail', verbose_name='submitted_suggestions'),
        ),
        migrations.AddField(
            model_name='suggestedantennadetailsuggestion',
            name='suggestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='suggestions.antennasuggestion', verbose_name='details'),
        ),
        migrations.AddField(
            model_name='suggestedcameradetailsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.cameradetail', verbose_name='submitted_suggestions'),
        ),
        migrations.AddField(
            model_name='suggestedcameradetailsuggestion',
            name='suggestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='suggestions.camerasuggestion', verbose_name='details'),
        ),
        migrations.AddField(
            model_name='suggestedframecameradetailsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.framecameradetail', verbose_name='submitted_suggestions'),
        ),
        migrations.AddField(
            model_name='suggestedframecameradetailsuggestion',
            name='suggestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_camera_details', to='suggestions.framesuggestion', verbose_name='details'),
        ),
        migrations.AddField(
            model_name='suggestedframemotordetailsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.framemotordetail', verbose_name='submitted_suggestions'),
        ),
        migrations.AddField(
            model_name='suggestedframemotordetailsuggestion',
            name='suggestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_motor_details', to='suggestions.framesuggestion', verbose_name='details'),
        ),
        migrations.AddField(
            model_name='suggestedframevtxdetailsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.framevtxdetail', verbose_name='submitted_suggestions'),
        ),
        migrations.AddField(
            model_name='suggestedframevtxdetailsuggestion',
            name='suggestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_vtx_details', to='suggestions.framesuggestion', verbose_name='details'),
        ),
        migrations.AddField(
            model_name='videoformatsuggestion',
            name='related_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.videoformat'),
        ),
        migrations.AddField(
            model_name='videoformatsuggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
