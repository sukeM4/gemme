# Generated by Django 3.1.5 on 2021-01-25 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20210122_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='img_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='img',
            field=models.ImageField(upload_to='images/2021/14/25'),
        ),
    ]
