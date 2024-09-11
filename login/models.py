from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# class Username(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Users')
#     image = models.ImageField(default='user/users.jpg', blank=True, upload_to='users/', verbose_name='Imagen de Perfil')
#
#     class Meta:
#         verbose_name = 'perfil'
#         verbose_name_plural = 'perfiles'
#         ordering = ['-id']
#
#     def __str__(self):
#         return self.user.username
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Username.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
