# Generated by Django 3.1.5 on 2021-03-09 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_auto_20210309_1255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='latitude',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='longitude',
            new_name='lon',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='latitude',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='longitude',
            new_name='lon',
        ),
    ]
