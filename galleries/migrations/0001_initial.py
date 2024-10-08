# Generated by Django 5.1.1 on 2024-10-08 17:53

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
            name='AntennaGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='components.antenna')),
            ],
            options={
                'ordering': ['order', '-created_at'],
                'abstract': False,
                'unique_together': {('object', 'order')},
            },
        ),
        migrations.CreateModel(
            name='CameraGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=galleries.mixins.upload_to_gallery)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='components.camera')),
            ],
            options={
                'ordering': ['order', '-created_at'],
                'abstract': False,
                'unique_together': {('object', 'order')},
            },
        ),
    ]