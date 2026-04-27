from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.Profile.models import Profile

User= get_user_model()

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwarge):
    
    if created:
        Profile.objects.create(user=instance)
        print(f"{instance}usercreate")
        