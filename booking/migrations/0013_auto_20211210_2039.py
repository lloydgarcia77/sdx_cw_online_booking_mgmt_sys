# Generated by Django 3.1.5 on 2021-12-10 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_auto_20211210_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walkininvoicemodel',
            name='slot',
            field=models.CharField(choices=[('1', 'Slot 1'), ('2', 'Slot 2'), ('3', 'Slot 3'), ('4', 'Slot 4'), ('5', 'Slot 5'), ('6', 'Slot 6')], default='Slot 1', max_length=10),
        ),
    ]
