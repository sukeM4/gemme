# Generated by Django 3.1.5 on 2021-03-21 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_auto_20210321_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='user',
        ),
    ]
