from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save



class Games(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, verbose_name="Game name")
    genre = models.CharField(max_length=60, verbose_name="Game genre")
    regular_price = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    release_date = models.DateField(verbose_name="Release")
    company = models.CharField(max_length=30, verbose_name="Company", default="MiroCoder")
    image = models.ImageField(upload_to='games/', null=True, blank=True, verbose_name="Game Image")

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return self.name

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True, verbose_name='Address', null=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name='Date of birth')
    games_lib = models.ManyToManyField(Games, blank=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    full_name = models.CharField(max_length=255, verbose_name='Name and Surname')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Sex')
    contact_number = models.CharField(max_length=20, verbose_name='Contact number', blank=True,null=True)

    class Meta:
        verbose_name = 'Gamer'
        verbose_name_plural = 'Gamers'

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        a = ProfileModel.objects.create(user=instance)
        a.save()
# Create your models here.
