# Generated by Django 3.1.5 on 2021-12-10 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20211209_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='InquiriesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=10)),
                ('l_name', models.CharField(max_length=10)),
                ('subject', models.CharField(max_length=10)),
                ('message', models.TextField()),
                ('email', models.EmailField(max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
