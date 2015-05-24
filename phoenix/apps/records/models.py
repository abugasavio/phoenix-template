from django.db import models
from smartmin.models import SmartModel


class AnimalNote(SmartModel):
    animal = models.ForeignKey('animals.Animal', null=False, blank=False)
    date = models.DateField(null=True, blank=True)
    file = models.FileField(max_length=100, upload_to='notes', null=True, blank=True)
    details = models.TextField(blank=True)


class AnimalDocument(SmartModel):
    file = models.FileField(upload_to='documents', max_length=255)
    animal = models.ForeignKey('animals.Animal', related_name='documents')
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Document of '%s'" % self.animal

    def delete(self):
        self.deleted = True
        self.save()

