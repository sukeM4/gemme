# Generated by Django 3.1.5 on 2021-02-05 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20210205_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='images/2021/25/05'),
        ),
    ]
