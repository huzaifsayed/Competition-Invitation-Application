from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

from .utils import unique_slug_generator

# Create your models here.
class CompetitionUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=12)
    email = models.EmailField(max_length = 254, unique=True) 
    slug = models.SlugField(max_length = 250, null = True, blank = True) 


class CompetitionInvite(models.Model):
    from_invite = models.ForeignKey(CompetitionUser, on_delete=models.CASCADE, related_name='from_invite')
    to_invite = models.ForeignKey(CompetitionUser, on_delete=models.CASCADE, related_name='to_invite')



def pre_save_receiver(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_slug_generator(instance) 

pre_save.connect(pre_save_receiver, sender = CompetitionUser) 