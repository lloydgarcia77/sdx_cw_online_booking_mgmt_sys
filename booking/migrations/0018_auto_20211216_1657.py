# Generated by Django 3.2.9 on 2021-12-16 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0017_auto_20211216_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoicebookingmodel',
            name='time_from',
        ),
        migrations.RemoveField(
            model_name='invoicebookingmodel',
            name='time_to',
        ),
        migrations.AddField(
            model_name='walkininvoicemodel',
            name='time_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='walkininvoicemodel',
            name='time_to',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
