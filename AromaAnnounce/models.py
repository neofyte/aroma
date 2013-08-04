from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from AromaNote.models import AromaNote
from AromaFriend.models import Relationship
from AromaFriend.signals import relationship_created

class AromaEvent(models.Model):
    
    content = models.CharField(max_length=150)
    announcer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='announcer_to_event', db_index=True)
    created_date = models.DateTimeField('时间', auto_now_add=True)

    content_type = models.ForeignKey(ContentType)  
    object_id = models.PositiveIntegerField()  
      
    event = generic.GenericForeignKey('content_type', 'object_id')  
      
    def __str__(self):
        return '{0} @ {1}'.format(self.owner, self.created_date)

    def description(self):  
        return self.event.description()


def AromaEvent_post_save(sender, instance, signal, *args, **kwargs):  
    post = instance  
    if post.created == post.updated:  
        event = Event(
        	content = post,
        	announcer = post.author,
        )  
        event.save()  
  
post_save.connect(AromaEvent_post_save, sender=AromaNote)
relationship_created.connect(AromaEvent_post_save, sender=Relationship)