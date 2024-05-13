import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal that CREATES a user profile anytime a user is created.
    When people create their User account, a profile will be automatically
    generated for them.
    """
    if created:
        if not hasattr(instance, 'profile'):

            profile = Profile.objects.create(user=instance)

            profile.username = instance.get_full_name() or instance.username
            profile.email = instance.email

            profile.save()

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Signal that saves 'Profile' instance whenever 'User' instance was updated.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    """
    Delete the user when the profile was deleted
    (e.g. if the admin decides to delete the profile)
    """
    try:
        user = User.objects.get(profile=instance)
    except User.DoesNotExist:
        user = None
    
    if user:
        try:
            print(f"Deleting user with ID {user.id} associated with profile ID {instance.id}")
            user.delete()
        except Exception as e:
            print(f"Error deleting user: {e}")
    else:
        print("No associated user found for the profile.")
