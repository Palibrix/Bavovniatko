from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from components.mixins.base_propeller_mixins import BasePropellerMixin
from components.models import Propeller
from suggestions.mixins import BaseSuggestionMixin, SuggestionFilesDeletionMixin, MediaHandlerMixin


class PropellerSuggestion(SuggestionFilesDeletionMixin, MediaHandlerMixin, BasePropellerMixin, BaseSuggestionMixin):

    related_instance = models.ForeignKey(
        'components.Propeller',
        blank=True,
        null=True,
        related_name='submitted_suggestions',
        on_delete=models.CASCADE
    )

    def _handle_post_accept(self, instance):
        self._handle_media(instance)

    def _create_instance(self):
        propeller = Propeller.objects.create(
            **{field: getattr(self, field)
               for field in self.PROPELLER_FIELDS}
        )

        propeller.full_clean()
        propeller.save()

        self.related_instance = propeller
        self.save()
        return propeller

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_propeller'
        verbose_name = _('Propeller Suggestion')
        verbose_name_plural = _('Propeller Suggestions')
        ordering = ['manufacturer', 'model']