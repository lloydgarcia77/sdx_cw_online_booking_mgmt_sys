# Generated by Django 3.2.9 on 2021-12-16 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0016_merge_0015_auto_20211211_1631_0015_auto_20211211_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicebookingmodel',
            name='time_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoicebookingmodel',
            name='time_to',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
