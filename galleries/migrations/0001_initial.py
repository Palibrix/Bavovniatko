# Generated by Django 5.1.5 on 2025-02-25 21:32

import django.db.models.deletion
import galleries.mixins
import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('components', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CameraGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Camera Gallery',
                'verbose_name_plural': 'Camera Galleries',
                'db_table': 'galleries_camera',
                'ordering': ['object', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DroneGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Drone Gallery',
                'verbose_name_plural': 'Drone Galleries',
            },
        ),
        migrations.CreateModel(
            name='FlightControllerGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Flight Controller Gallery',
                'verbose_name_plural': 'Flight Controller Galleries',
                'db_table': 'galleries_flight_controller',
                'ordering': ['object', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FrameGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Frame Gallery',
                'verbose_name_plural': 'Frame Galleries',
                'db_table': 'galleries_frame',
                'ordering': ['object', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MotorGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Motor Gallery',
                'verbose_name_plural': 'Motor Galleries',
                'db_table': 'galleries_motor',
                'ordering': ['object', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PropellerGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Propeller Gallery',
                'verbose_name_plural': 'Propeller Galleries',
                'db_table': 'galleries_propeller',
                'ordering': ['object', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReceiverGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Receiver Gallery',
                'verbose_name_plural': 'Receiver Galleries',
                'db_table': 'galleries_receiver',
                'ordering': ['object', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SpeedControllerGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Speed Controller Gallery',
                'verbose_name_plural': 'Speed Controller Galleries',
                'db_table': 'galleries_speed_controller',
                'ordering': ['object', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='StackGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Stack Gallery',
                'verbose_name_plural': 'Stack Galleries',
                'db_table': 'galleries_stack',
                'ordering': ['object', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TransmitterGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Transmitter Gallery',
                'verbose_name_plural': 'Transmitter Galleries',
                'db_table': 'galleries_transmitter',
                'ordering': ['object', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AntennaGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='components.antenna')),
            ],
            options={
                'verbose_name': 'Antenna Gallery',
                'verbose_name_plural': 'Antenna Galleries',
                'db_table': 'galleries_antenna',
                'ordering': ['object', 'order', '-created_at'],
            },
        ),
    ]
