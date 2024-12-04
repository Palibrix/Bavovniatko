# Generated by Django 5.1.3 on 2024-12-02 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestions', '0002_antennasuggestion_admin_comment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AntennaConnectorSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(help_text='Type of antenna connector', max_length=50, unique=True)),
                ('reviewed', models.BooleanField(default=False)),
                ('admin_comment', models.TextField(blank=True, null=True)),
                ('request_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Antenna Type Connector',
                'verbose_name_plural': 'Antenna Type Connectors',
                'db_table': 'suggestions_antenna_connector',
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='AntennaTypeSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(help_text='Type of the antenna, e.g. Monopole, Dipole etc.', max_length=50, unique=True)),
                ('direction', models.CharField(choices=[('directional', 'Directional'), ('omni', 'Omni-directional')], default='directional', help_text='Omni-directional: all directions, Directional: one direction.', max_length=50)),
                ('polarization', models.CharField(choices=[('linear', 'Linear, LP'), ('left_circular', 'Left-hand Circular, LHCP'), ('right_circular', 'Right-hand Circular, RHCP')], default='linear', max_length=50)),
                ('reviewed', models.BooleanField(default=False)),
                ('admin_comment', models.TextField(blank=True, null=True)),
                ('request_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Antenna Type Suggestion',
                'verbose_name_plural': 'Antenna Type Suggestions',
                'db_table': 'suggestions_antenna_type',
                'ordering': ['type'],
            },
        ),
    ]
