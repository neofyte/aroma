from django.db import models
from django.conf import settings

from utils.signals import paper_entry_created

from .validator import validate_identifier
from AromaAnnounce.models import AromaEvent

class AromaPaperEntry(models.Model):

    title = models.CharField(max_length=100)
    identifier = models.CharField(max_length=20, validators=[validate_identifier], blank=True)
    abstract = models.CharField(max_length=1000, blank=True)
    author = models.CharField(max_length=100, db_index=True)
    # will establish a separate model for paper subjects
    category = models.CharField(max_length=15, blank=True)
    submitted = models.DateTimeField(blank=True)

    # add by clean method in AromaPaperForm
    abs_url = models.URLField()

    # aroma data
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='UserToPaper')

    #trace aromanote back to the event, maybe useless
    #events = generic.GenericRelation(AromaEvent)

    def __str__(self):
        return self.title
    
    @property
    def description(self):  
        return '{0} added {1}'.format(self.creator, self.title)

    @property
    def announcer(self):
        return self.creator

    def save(self, *args, **kwargs):
        self.abs_url=''.join(['arxiv.org/abs', self.identifier.split(':')[-1]])
        super(AromaPaperEntry,self).save(*args,**kwargs)
        AromaPaperEntry.send(sender=AromaPaperEntry, instance=self)

paper_entry_created.connect(
    AromaEvent.AromaEvent_post_save, sender=AromaPaperEntry, dispatch_uid="AromaPaperEntry"
)
