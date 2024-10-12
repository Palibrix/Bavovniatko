# Generated by Django 5.1.2 on 2024-10-10 21:30

import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('components', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(blank=True, max_length=50, null=True)),
                ('model', models.CharField(help_text='Full name of the Drone', max_length=50)),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, help_text='Long description of the Drone', verbose_name='Text')),
                ('short_description', models.CharField(blank=True, help_text='Short description of the Drone', max_length=256, null=True)),
                ('type', models.CharField(choices=[('photography', 'Photography'), ('sport', 'Sport'), ('freestyle', 'Freestyle'), ('another', 'Another')], default='photography', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('antenna', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.antenna')),
                ('battery', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.battery')),
                ('camera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.camera')),
                ('flight_controller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.flightcontroller')),
                ('frame', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.frame')),
                ('motor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.motor')),
                ('propeller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.propeller')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.receiver')),
                ('speed_controller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.speedcontroller')),
                ('transmitter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='components.transmitter')),
            ],
            options={
                'verbose_name': 'Drone',
                'verbose_name_plural': 'Drones',
                'db_table': 'builds_drone',
                'ordering': ('manufacturer', 'model'),
                'unique_together': {('manufacturer', 'model')},
            },
        ),
    ]
