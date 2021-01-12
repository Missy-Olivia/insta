from django.db import models
import datetime as dt
from tinymce.models import HTMLField
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    profile_photo= models.ImageField(upload_to='profiles/',null=True)
    bio= models.CharField(max_length=140, null=True)


    def save_profile(self):
        self.save()

    @classmethod
    def get_profile(cls, user):
        profile = cls.objects.filter(user=user).first()
        return profile

    @classmethod
    def get_profile_id(cls, user):
        profile = cls.objects.get(pk =user)
        return profile

    @classmethod
    def find_profile(cls,search_term):
        profile = Profile.objects.filter(user__username__icontains=search_term)
        return profile

    class Meta:
        ordering = ['user']
