from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)

    is_staff = models.BooleanField(default=False,
                                   help_text=_('Designates whether the user can log into this admin site'),
                                   verbose_name=_('Staff status'))
    is_active = models.BooleanField(default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. '
                                        'Unselect this instead of deleting accounts'),
                                    verbose_name=_('Active'))
    is_superuser =  models.BooleanField(default=False,
                                         help_text=_('Designates that this user has all permissions '
                                                     'without explicitly assigning them.'),
                                         verbose_name=_('Superuser status'))

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("Date joined"))
    last_login = models.DateTimeField(blank=True, null=True, verbose_name=_('Last login'))

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user = User.objects.get(username=self.username)
        from users.models import Profile
        if not Profile.objects.filter(user=user).exists():
            profile = Profile.objects.create(user=user)
            profile.save()

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'users'
        db_table = 'users_user'

        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['id']
