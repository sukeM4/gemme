# Generated by Django 3.1.5 on 2021-04-27 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0031_auto_20210427_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
