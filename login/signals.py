from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# from login.models import Username


# @receiver(post_save, sender=Username)
# def add_user_group(sender, instance, created, **kwargs):
#     if created:
#         try:
#             secretary = Group.objects.get(name='secretary')
#         except Group.DoesNotExist:
#             secretary = Group.objects.create(name='secretary')
#         instance.user.groups.add(secretary)
