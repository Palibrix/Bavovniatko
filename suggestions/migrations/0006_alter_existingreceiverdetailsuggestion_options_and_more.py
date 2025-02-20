# Generated by Django 5.1.5 on 2025-02-20 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestions', '0005_existingreceiverdetailsuggestion_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='existingreceiverdetailsuggestion',
            options={'ordering': ['receiver', 'frequency'], 'verbose_name': 'Existing Receiver Detail Suggestion', 'verbose_name_plural': 'Existing Receiver Detail Suggestions'},
        ),
        migrations.AlterModelOptions(
            name='receiverprotocoltypesuggestion',
            options={},
        ),
        migrations.AlterModelOptions(
            name='receiversuggestion',
            options={},
        ),
        migrations.AlterModelOptions(
            name='suggestedreceiverdetailsuggestion',
            options={'ordering': ['related_instance', 'frequency'], 'verbose_name': 'Suggested Receiver Detail', 'verbose_name_plural': 'Suggested Receiver Details'},
        ),
        migrations.AlterField(
            model_name='receiverprotocoltypesuggestion',
            name='type',
            field=models.CharField(help_text='Rx To FC', max_length=50, unique=True, verbose_name='Output Protocol Type'),
        ),
        migrations.AlterModelTable(
            name='receiverprotocoltypesuggestion',
            table=None,
        ),
        migrations.AlterModelTable(
            name='receiversuggestion',
            table=None,
        ),
    ]
