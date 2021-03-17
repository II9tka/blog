from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from colorfield.fields import ColorField
from enumfields import Enum, EnumIntegerField
from backend.utils.models import BaseQuerySet

__all__ = (
    'Account',
    'AccountPrivacyStatus',
)


class AccountPrivacyStatus(Enum):
    PRIVATE = 0
    PUBLIC = 1

    class Labels:
        PRIVATE = _('Private')
        PUBLIC = _('Public')


class AccountGender(Enum):
    NOT_SPECIFIED = 0
    MALE = 1
    FEMALE = 2

    class Labels:
        NOT_SPECIFIED = _('Not specified')
        MALE = _('Male')
        FEMALE = _('Female')


class AccountManager(UserManager.from_queryset(BaseQuerySet)):
    pass


class Account(AbstractUser):
    COMMON_PREFETCH_RELATED = ('images',)

    status_type = EnumIntegerField(
        AccountPrivacyStatus, default=AccountPrivacyStatus.PUBLIC, help_text=_(
            'Account publicity status.'
        ), verbose_name=_('Status type')
    )
    gender = EnumIntegerField(
        AccountGender, default=AccountGender.NOT_SPECIFIED, verbose_name=_('Gender')
    )
    background_color = ColorField(
        default='#FFFFFF', format='hexa', help_text=_(
            'User can customize background color of the account. \n'
            'Default color is White (#FFFFFF)'
        ), verbose_name=_('Background color')
    )
    city = models.CharField(
        max_length=100, blank=True, default='', help_text=_(
            'User\'s hometown name. Max length is 100.'
        ), verbose_name=_('City')
    )
    phone_number = PhoneNumberField(
        blank=True, verbose_name=_('Phone')
    )
    workplace = models.CharField(
        max_length=150, blank=True, default='', help_text=_(
            'User\'s workplace. Max length is 150.'
        ), verbose_name=_('Workplace')
    )
    work_experience = models.TextField(
        max_length=2000, blank=True, default='', help_text=_(
            'User can specify work experience. Max length is 2000.'
        ), verbose_name=_('Work experience')
    )
    about = models.TextField(
        blank=True, default='', max_length=2000, help_text=_(
            'User information about myself. Max length is 2000.'
        ), verbose_name=_('About')
    )

    objects = AccountManager()

    def truncate_about(self):
        if len(self.about) > 100:
            return self.about[:100] + '...'
        return self.about

    def last_image(self):
        if images := self.images:
            return images.last().get_image()
        return None

    def __str__(self):
        return 'User %i' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
