from django.db import models
from datetime import datetime
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Store(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.CharField(max_length=200)
    lon = models.DecimalField(
        max_digits=9, decimal_places=7, null=True, blank=True)
    lat = models.DecimalField(
        max_digits=9, decimal_places=7, null=True, blank=True)
    # visitors
    visits = models.IntegerField(default=0)
    img = models.ImageField(
        upload_to=f"images/{datetime.strftime(datetime.now(), '%Y/%m/%d')}", blank=True, null=True)

    def __str__(self):
        return self.user.username


class Caption(models.Model):
    text = models.TextField()


class Tag(models.Model):
    title = models.CharField(max_length=20)


class Url(models.Model):
    url = models.URLField()


class Item(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ForeignKey(
        Tag, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True, null=True)
    img_url = models.URLField(blank=True, null=True)
    
    height_field = models.PositiveIntegerField(blank=True, null=True)
    width_field = models.PositiveIntegerField(blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=100, blank=True)

    is_sold = models.BooleanField(default=False)
    is_ad = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)

    # visitors
    visits = models.IntegerField(default=0)
    date_crawled = models.DateField(auto_now_add=True)
    
    def image_directory_path(instance, filename):
        return f"images/{datetime.strftime(instance.date_crawled, '%Y/%m/%d')}/{filename}"

    img = models.ImageField(upload_to=image_directory_path,
                            height_field='height_field', width_field='width_field', blank=True, null=True)
    # cordinates
    lon = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.title.upper()

wa = 'whatsapp'
nc = 'normal calls'
contact_choices = ((wa, 'whatsapp'),
                   (nc, 'normal calls'))


class ItemContact(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, choices=contact_choices, blank=True,)

@receiver(pre_delete, sender=Item)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.img.delete(False)


@receiver(post_save, sender=User)
def create_store_profile(sender, instance, created, **kwargs):
    if created:
        Store.objects.create(user=instance)
