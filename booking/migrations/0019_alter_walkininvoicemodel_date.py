# Generated by Django 3.2.9 on 2021-12-16 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0018_auto_20211216_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walkininvoicemodel',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
