# Generated by Django 3.1.5 on 2021-12-10 08:06

import booking.file_validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_auto_20211210_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='staff_images/', validators=[booking.file_validators.file_validator_image])),
                ('f_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('m_name', models.CharField(max_length=50, verbose_name='Middle Name')),
                ('l_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=50)),
                ('dob', models.DateField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('position', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('contact_no', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='Contact No')),
                ('date_added', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
