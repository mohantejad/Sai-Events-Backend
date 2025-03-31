import os
from django.db import models
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.translation import gettext_lazy as _



pp_fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "profile_pictures"))

class Event(models.Model):
    class ModeChoices(models.TextChoices):
        ONSITE = 'On Site'
        HYBRID = 'Hybrid'
        ONLINE = 'Online'

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events"
    )
    organization = models.TextField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        _('event_image'),
        storage=pp_fs,
        blank=True,
        null=True
    )
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=now)
    category = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    mode = models.TextField(choices=ModeChoices, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title
