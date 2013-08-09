from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.dispatch import Signal, receiver

from AromaFriend.models import Relationship
from AromaFriend.signals import relationship_created

class AromaEvent(models.Model):
    
    content = models.CharField(max_length=150)
    announcer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='announcer_to_event', db_index=True)
    created_date = models.DateTimeField('时间', auto_now_add=True)

    content_type = models.ForeignKey(ContentType)  
    object_id = models.PositiveIntegerField()  
      
    event = generic.GenericForeignKey()  
      
    def __str__(self):
        return '{0} @ {1}'.format(self.owner, self.created_date)

    @property
    def description(self):  
        return self.event.description

    @classmethod
    def AromaEvent_post_save(self, sender, instance, *args, **kwargs):  
        event = AromaEvent(
            content = instance.description,
            announcer = instance.announcer,
            event = instance,
        )  
        event.save()  
  

#relationship_created.connect(AromaEvent_post_save, sender=Relationship)