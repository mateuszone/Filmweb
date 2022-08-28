from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from basic.models import Profile


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
