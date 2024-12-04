from abc import abstractmethod

from django.db import models


class BaseSuggestionMixin(models.Model):
    reviewed = models.BooleanField(default=False)
    admin_comment = models.TextField(blank=True, null=True)
    request_description = models.TextField(blank=True, null=True)

    @abstractmethod
    def accept(self):
        pass

    def deny(self):
        self.reviewed = True
        self.save()

    class Meta:
        abstract = True