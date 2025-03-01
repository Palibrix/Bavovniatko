from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.mixins import SuggestionActionsMixin
from api.v1.galleries.mixins import GalleryContextMixin
from api.v1.suggestions.serializers.propeller_suggestion_serializers import PropellerSuggestionSerializer
from suggestions.models import PropellerSuggestion
from users.permissions import HasAcceptDeny


class PropellerSuggestionAPIViewSet(GalleryContextMixin, SuggestionActionsMixin, ModelViewSet):
    permission_classes = (IsAuthenticated, HasAcceptDeny)
    model = PropellerSuggestion
    serializer_class = PropellerSuggestionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return PropellerSuggestion.objects.distinct()
        else:
            return PropellerSuggestion.objects.filter(user=self.request.user).distinct()
