# Generated by Django 5.0.4 on 2024-05-01 19:46

import components.mixins
import components.validators
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0003_alter_framedetail_frame'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AntennaConnector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(help_text='Type of antenna connector', max_length=50)),
                ('is_custom', models.BooleanField(default=True, help_text='Created by user?')),
            ],
            options={
                'verbose_name': 'Antenna Connector',
                'verbose_name_plural': 'Antenna Connectors',
                'ordering': ['type', '-is_custom'],
            },
        ),
        migrations.CreateModel(
            name='ReceiverProtocol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(help_text='Rx To FC', max_length=50, verbose_name='Output Protocol Type')),
                ('is_custom', models.BooleanField(default=True, help_text='Created by user?')),
            ],
            options={
                'verbose_name': 'Receiver Protocol',
                'verbose_name_plural': 'Receiver Protocols',
                'ordering': ['type', '-is_custom'],
            },
        ),
        migrations.RemoveField(
            model_name='camera',
            name='height',
        ),
        migrations.RemoveField(
            model_name='camera',
            name='height_bracket',
        ),
        migrations.RemoveField(
            model_name='camera',
            name='width',
        ),
        migrations.RemoveField(
            model_name='camera',
            name='width_bracket',
        ),
        migrations.AlterField(
            model_name='framedetail',
            name='frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frame_details', to='components.frame'),
        ),
        migrations.CreateModel(
            name='CameraDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.FloatField(help_text='Height of the camera in mm', max_length=5, verbose_name='Camera mount size height')),
                ('width', models.FloatField(help_text='Width of the camera in mm', max_length=5, verbose_name='Camera mount size width')),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.camera')),
            ],
        ),
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=50)),
                ('model', models.CharField(help_text='Full name of the item', max_length=50)),
                ('processor', models.CharField(blank=True, help_text='Name of the processor', max_length=100, null=True)),
                ('voltage_min', models.FloatField(help_text='Voltage Range - Minimal Voltage', validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(28)], verbose_name='Minimal Voltage')),
                ('voltage_max', models.FloatField(blank=True, help_text='Voltage Range - Maximal Voltage', null=True, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(28)], verbose_name='Maximal Voltage')),
                ('antenna_connector', models.ManyToManyField(to='components.antennaconnector')),
                ('user', models.ForeignKey(blank=True, help_text='Public if empty', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('protocol', models.ManyToManyField(help_text='Rx To FC', to='components.receiverprotocol', verbose_name='Output Protocol')),
            ],
            options={
                'verbose_name': 'Receiver',
                'verbose_name_plural': 'Receivers',
                'ordering': ['manufacturer', 'model'],
            },
            bases=(models.Model, components.mixins.UniqueConstraintMixin),
        ),
        migrations.CreateModel(
            name='ReceiverDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.FloatField(validators=[components.validators.validate_even_number])),
                ('weight', models.FloatField(validators=[components.validators.validate_even_number])),
                ('telemetry_power', models.FloatField(help_text='Telemetry Power, In dBm', validators=[components.validators.validate_even_number])),
                ('rf_chip', models.CharField(blank=True, help_text='RF Chip Number', max_length=50, null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receiver_details', to='components.receiver')),
            ],
            options={
                'verbose_name': 'Receiver Detail',
                'verbose_name_plural': 'Receiver Details',
                'ordering': ['receiver', 'frequency', 'weight', 'telemetry_power', 'rf_chip'],
            },
        ),
    ]
