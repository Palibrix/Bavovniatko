# Generated by Django 5.1.5 on 2025-02-15 20:04

import django.core.validators
import django.db.models.deletion
import django_ckeditor_5.fields
import suggestions.mixins
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0002_alter_motordetail_voltage_and_more'),
        ('suggestions', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExistingMotorDetailSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('weight', models.FloatField(help_text='Motor weight in grams', validators=[django.core.validators.MinValueValidator(0)])),
                ('max_power', models.PositiveIntegerField(help_text='Max power, W')),
                ('kv_per_volt', models.PositiveIntegerField(help_text='KV per volt', verbose_name='KV per volt')),
                ('peak_current', models.FloatField(blank=True, help_text='Peak current of the motor, A', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('idle_current', models.FloatField(blank=True, help_text='Idle current of the motor, A', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('resistance', models.FloatField(blank=True, help_text='Resistance, in mΩ (mOhm)', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Internal Resistance')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending', max_length=20)),
                ('admin_comment', models.TextField(blank=True, null=True)),
                ('request_description', models.TextField(blank=True, null=True)),
                ('motor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='components.motor', verbose_name='Motor')),
                ('related_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='components.motordetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('voltage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_rated_voltage', to='components.ratedvoltage')),
            ],
            options={
                'verbose_name': 'Existing Motor Detail Suggestion',
                'verbose_name_plural': 'Existing Motor Detail Suggestions',
                'db_table': 'suggestions_existing_motor_detail',
                'ordering': ['motor'],
            },
        ),
        migrations.CreateModel(
            name='MotorSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('manufacturer', models.CharField(max_length=50)),
                ('model', models.CharField(help_text='Full name of the item', max_length=50)),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, help_text='Long description of the item', verbose_name='Text')),
                ('stator_diameter', models.CharField(help_text='Two first digits of size (e.g. 28 from 2806)', max_length=2, validators=[django.core.validators.MinLengthValidator(2)])),
                ('stator_height', models.CharField(help_text='Two last digits of size (e.g. 06 from 2806 or 06.5 from 2806.5)', max_length=4, validators=[django.core.validators.MinLengthValidator(2)])),
                ('configuration', models.CharField(help_text='Configuration of the motor (e.g. 12N14P)', max_length=50)),
                ('mount_height', models.FloatField(help_text='Height of the motor in mm', max_length=5, verbose_name='Motor mount size height')),
                ('mount_width', models.FloatField(help_text='Width of the motor in mm', max_length=5, verbose_name='Motor mount size width')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending', max_length=20)),
                ('admin_comment', models.TextField(blank=True, null=True)),
                ('request_description', models.TextField(blank=True, null=True)),
                ('related_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.motor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Motor Suggestion',
                'verbose_name_plural': 'Motor Suggestions',
                'db_table': 'suggestions_motor',
                'ordering': ['manufacturer', 'model'],
            },
            bases=(suggestions.mixins.MediaHandlerMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RatedVoltageSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('min_cells', models.IntegerField(default=1, help_text='Number of min. possible quantity of cells in series', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Min. number of cells')),
                ('max_cells', models.IntegerField(default=1, help_text='Number of max. possible quantity of cells in series', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Max. number of cells')),
                ('type', models.CharField(choices=[('LIPO', 'LiPo'), ('LI_ION', 'Li-Ion'), ('LIHV', 'LiHV'), ('ANOTHER', 'Another')], default='LIPO', max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending', max_length=20)),
                ('admin_comment', models.TextField(blank=True, null=True)),
                ('request_description', models.TextField(blank=True, null=True)),
                ('related_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.ratedvoltage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Rated Voltage Suggestion',
                'verbose_name_plural': 'Rated Voltage Suggestions',
                'db_table': 'suggestions_rated_voltage',
                'ordering': ['min_cells', 'max_cells'],
            },
        ),
        migrations.CreateModel(
            name='SuggestedMotorDetailSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('weight', models.FloatField(help_text='Motor weight in grams', validators=[django.core.validators.MinValueValidator(0)])),
                ('max_power', models.PositiveIntegerField(help_text='Max power, W')),
                ('kv_per_volt', models.PositiveIntegerField(help_text='KV per volt', verbose_name='KV per volt')),
                ('peak_current', models.FloatField(blank=True, help_text='Peak current of the motor, A', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('idle_current', models.FloatField(blank=True, help_text='Idle current of the motor, A', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('resistance', models.FloatField(blank=True, help_text='Resistance, in mΩ (mOhm)', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Internal Resistance')),
                ('related_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_suggestions', to='components.motordetail', verbose_name='submitted_suggestions')),
                ('suggestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_details', to='suggestions.motorsuggestion', verbose_name='details')),
                ('voltage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_rated_voltage', to='components.ratedvoltage')),
            ],
            options={
                'verbose_name': 'Suggested Motor Detail',
                'verbose_name_plural': 'Suggested Motor Details',
                'db_table': 'suggestions_suggested_motor_detail',
                'ordering': ['related_instance'],
            },
        ),
    ]
