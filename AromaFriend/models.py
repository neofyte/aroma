from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.conf import settings

from .signals import relationship_created

User = settings.AUTH_USER_MODEL


class Relationship(models.Model):

    from_user = models.ForeignKey(User, related_name="froms_rel")
    to_user = models.ForeignKey(User, related_name="tos_rel")
    
    class Meta:
        unique_together = [("from_user", "to_user")]

    def clean(self):
        super(Relationship, self).clean()
        if self.from_user == self.to_user:
            raise ValidationError(
                "User cannot form a relationship with themselves."
            )
        followship = Relationship.objects.filter(
            Q(from_user=self.from_user, to_user=self.to_user)
        )
        if followship is not None:
            raise ValidationError(
                "Relationship between {0} and {1} already exists.".format(
                    self.from_user, self.to_user
                )
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pk is None:
            created = True
        else:
            created = False
        followship = super(Relationship, self).save(*args, **kwargs)
        if created:
            relationship_created.send(
                sender=Relationship,
                relationship=followship
            )
        return followship
