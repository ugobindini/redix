# Generated by Django 4.0.6 on 2023-10-19 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redix', '0014_point_len_segment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='point',
            name='len_segment',
        ),
    ]