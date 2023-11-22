from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save, pre_save
import pathlib
MEDIA_ROOT = settings.MEDIA_ROOT

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, full_name, email, username, password = None , **other_fields):
        other_fields.setdefault('is_active', True)
        
        if not full_name:
            raise ValueError('full_name can not be blank')
        if not email:
            raise ValueError("All users must have an email")
        if not username:
            raise ValueError('username can not be blank, kindly fill in your username')

        email = self.normalize_email(email)
        user = self.model(full_name=full_name, email=email, username=username, password=password, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_staffuser(self, full_name, email, username, password=None, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)


        if not other_fields.get('is_active'):
            raise ValueError('Staff users must have an active account')
        user = self.create_user(
            full_name=full_name,
            email=email,
            username=username,
            password=password,
            **other_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, username, password = None, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if not other_fields.get('is_active'):
            raise ValueError('Staff users must have an active account')

        if not other_fields.get('is_staff'):
            raise ValueError('All Superusers must have a staff account')
        user = self.create_user(
            full_name=full_name,
            email=email,
            username=username,
            password = password,
            **other_fields
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=250, unique=True)
    email = models.EmailField(verbose_name='Email', unique=True)
    username= models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['full_name', 'username']
    USERNAME_FIELD = 'email'

    objects = UserManager()


    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name = 'profile', on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    # url = models.URLField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, default=f'{MEDIA_ROOT}/user_photo.png')
    date_created = models.DateTimeField(auto_now_add=True)

def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user = instance, username = instance.full_name, email = instance.email)

def save_user_profile(sender, instance, created, *args, **kwargs):
    instance.profile.save()

def update_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        instance.username = instance.user.full_name
        instance.email = instance.user.email
        instance.save()

       

def pre_save_profile(sender, instance, *args, **kwargs):
    if not instance.username:
        instance.username = instance.user.full_name
    if not instance.email:
        instance.email = instance.user.email
    if not instance.profile_image:
        instance.profile_image = f'{MEDIA_ROOT}/user_photo.png'



pre_save.connect(pre_save_profile, sender=Profile)
post_save.connect(update_user_profile, sender=Profile)   

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)