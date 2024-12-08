from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username if hasattr(self.user, 'username') else ''

    class Meta:
        app_label = 'users'
        db_table = 'users_profile'

        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ['id']