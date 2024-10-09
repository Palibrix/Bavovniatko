from ckeditor.fields import RichTextField
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


class BaseModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class BaseComponentMixin(BaseModelMixin):
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50, help_text=_("Full name of the item"))
    description = CKEditor5Field('Text', blank=True, help_text=_("Long description of the item"))

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

    class Meta:
        abstract = True
        unique_together = (('manufacturer', 'model',),)


class BaseModelAdminMixin(admin.ModelAdmin):
    empty_value_display = '???'
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_display_links = ('__str__', )
