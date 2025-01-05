from abc import abstractmethod

from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.http import HttpResponseRedirect

from components.mixins import BaseModelAdminMixin

User = get_user_model()

class BaseSuggestionFilesDeletionMixin(models.Model):

    @transaction.atomic
    def delete(self, *args, **kwargs):
        for image in self.suggested_images.all():
            if not image.object:
                image.delete()

        for file in self.suggested_documents.all():
            if not file.object:
                file.delete()

        super().delete(*args, **kwargs)

    class Meta:
        abstract = True

class BaseSuggestionMixin(models.Model):
    reviewed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    admin_comment = models.TextField(blank=True, null=True)
    request_description = models.TextField(blank=True, null=True)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)

    @abstractmethod
    def accept(self):
        pass

    def deny(self, admin_comment=None):
        self.reviewed = True
        self.accepted = False
        if admin_comment:
            self.admin_comment = admin_comment
        self.save()

    class Meta:
        abstract = True

    @classmethod
    def _check_fields(cls, **kwargs):
        cls._meta.get_field('related_instance')
        return super()._check_fields(**kwargs)


@admin.action(description="Accept selected suggestions")
def accept_suggestions(modeladmin, request, queryset):
    for suggestion in queryset:
        suggestion.accept()
    messages.success(request, "Selected suggestions have been accepted.")

@admin.action(description="Deny selected suggestions")
def deny_suggestions(modeladmin, request, queryset):
    for suggestion in queryset:
        suggestion.deny()
    messages.success(request, "Selected suggestions have been denied.")


class BaseSuggestionAdminMixin(BaseModelAdminMixin):
    actions = [accept_suggestions, deny_suggestions]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            # Remove the actions if the user is not a superuser
            actions.pop(accept_suggestions.__name__)
            actions.pop(deny_suggestions.__name__)
        return actions

    def response_change(self, request, obj):
        if "_accept" in request.POST:
            try:
                obj.accept()
                self.message_user(request, 'Suggestion has been accepted', messages.SUCCESS)
            except ValidationError as e:
                error_message = ''
                if '__all__' in e.message_dict:
                    error_message = e.message_dict['__all__'][0]
                else:
                    for field, errors in e.message_dict.items():
                        error_message += '{}: {} '.format(field, ', '.join(errors))
                self.message_user(request, 'Error accepting suggestion: {}'.format(error_message), messages.ERROR)
                return HttpResponseRedirect(request.path)
            except Exception as e:
                self.message_user(request, 'An error occurred: {}'.format(e), messages.ERROR)

        elif "_deny" in request.POST:
            obj.deny()
            msg = 'Suggestion has been denied'
            messages.success(request, msg)
        return super().response_change(request, obj)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super().add_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
