# Generated by Django 3.1.5 on 2021-12-09 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20211209_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingmodel',
            name='time_slot',
            field=models.CharField(choices=[('1', '8:00am - 10:00am'), ('2', '10:00am - 12:00pm'), ('3', '12:00pm- 2:00pm'), ('4', '2:00pm - 4:00pm'), ('5', '4:00pm - 6:00pm'), ('6', '6:00pm - 8:00pm')], default='1', max_length=2),
        ),
    ]
