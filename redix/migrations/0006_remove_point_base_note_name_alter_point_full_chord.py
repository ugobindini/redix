# Generated by Django 4.0.6 on 2023-09-30 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redix', '0005_rename_filename_point_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='point',
            name='base_note_name',
        ),
        migrations.AlterField(
            model_name='point',
            name='full_chord',
            field=models.JSONField(),
        ),
    ]
