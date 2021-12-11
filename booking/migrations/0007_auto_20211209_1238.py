# Generated by Django 3.1.5 on 2021-12-09 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20211209_1226'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='bookingmodel',
            name='unique time slot',
        ),
        migrations.AddConstraint(
            model_name='bookingmodel',
            constraint=models.UniqueConstraint(fields=('date', 'slot', 'time_slot'), name='unique time slot'),
        ),
    ]
