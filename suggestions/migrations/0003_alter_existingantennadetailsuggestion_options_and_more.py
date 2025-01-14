# Generated by Django 5.1.3 on 2025-01-14 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0001_initial'),
        ('suggestions', '0002_rename_antenna_suggestedantennadetailsuggestion_suggestion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='existingantennadetailsuggestion',
            options={'ordering': ['antenna', 'connector_type'], 'verbose_name': 'Existing Antenna Detail Suggestion', 'verbose_name_plural': 'Existing Antenna Detail Suggestions'},
        ),
        migrations.AlterUniqueTogether(
            name='existingantennadetailsuggestion',
            unique_together={('antenna', 'connector_type', 'angle_type')},
        ),
    ]
