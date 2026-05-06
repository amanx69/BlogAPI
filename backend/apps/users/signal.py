from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.Profile.models import Profile
from apps.Profile.service import gernate_username

User= get_user_model()

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwarge):
    
    if created:
        username =gernate_username(instance.email)
        Profile.objects.create(user=instance,username=username)
        print(f"{instance}usercreate")
        