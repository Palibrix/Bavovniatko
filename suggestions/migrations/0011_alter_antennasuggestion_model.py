# Generated by Django 5.1.5 on 2025-01-21 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestions', '0010_alter_antennaconnectorsuggestion_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antennasuggestion',
            name='model',
            field=models.CharField(help_text='Full name of the item', max_length=50),
        ),
    ]
