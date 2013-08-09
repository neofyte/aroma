from django.db import models
from django.conf import settings

from django.db.models.signals import post_save
from utils.signals import note_created

from AromaAnnounce.models import AromaEvent

class AromaNote(models.Model):

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='AnnounceToNote')
    created = models.DateTimeField('发表时间', auto_now_add=True, blank=True)
    updated = models.DateTimeField('最后修改时间', blank=True)

    #trace aromanote back to the event, maybe useless
    #events = generic.GenericRelation(AromaEvent)

    def __str__(self):
        return self.title
    
    @property
    def description(self):  
        return u'{0} 发表《{1}》'.format(self.author, self.title)

    @property
    def announcer(self):
        return self.author

    def save(self, *args, **kwargs):
        super(AromaNote,self).save(*args,**kwargs)
        note_created.send(sender=AromaNote, instance=self)

note_created.connect(AromaEvent.AromaEvent_post_save, sender=AromaNote, dispatch_uid="AromaNote")