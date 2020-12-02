from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class ApiHit(models.Model):
    # noinspection PyPep8Naming
    class ACTION_CHOICES(models.TextChoices):
        BASIC_INFO = 'basic_info', _('Basic Info')
        KIOSK = 'kiosk', _('Kiosk')
        JSON = 'json', _('Json Response')
        REDIRECT = 'redirect', _('Redirect')

    hit_date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(
        max_length=16, choices=ACTION_CHOICES.choices, default=ACTION_CHOICES.BASIC_INFO)
    code = models.ForeignKey(
        'QRCode', on_delete=models.CASCADE, related_name='hits')


class Department(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'


class LinkUrl(models.Model):
    name = models.CharField(max_length=64, blank=True,
                            default='', help_text='Name of the url. Used in buttons and links when a code is scanned.')
    url = models.URLField(blank=True,
                          default='',
                          help_text='redirect to external page')
    priority = models.FloatField(default=1)
    code = models.ForeignKey(
        to='QRCode',
        on_delete=models.CASCADE,
        related_name='urls')

    class Meta:
        ordering = ['-priority']


QR_MODE_HELP_TEXT = """
Sets the mode this code is in.<br/>
Kiosk Mode: Show buttons to choose a link from<br/>
Redirect Mode: Instantly redirects to the url with the highest priority.<br/>
Information Page Mode: Show basic info with links to different urls
"""


class QRCode(models.Model):
    # noinspection PyPep8Naming
    class REDIRECT_MODE_CHOICES(models.TextChoices):
        KIOSK = 'kiosk', _('Kiosk Mode')
        REDIRECT = 'redirect', _('Redirect Mode')
        INFO_PAGE = 'info_page', _('Information Page Mode')

    title = models.CharField(blank=True, default='', max_length=100)
    department = models.ForeignKey(
        to=Department, on_delete=models.CASCADE)

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=True
    )

    basic_info = models.TextField(blank=True, default='')

    mode = models.CharField(
        max_length=16, choices=REDIRECT_MODE_CHOICES.choices, default=REDIRECT_MODE_CHOICES.REDIRECT,
        help_text=QR_MODE_HELP_TEXT)

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    extra_data = models.JSONField(default=dict, blank=True,
                                  help_text='Use this to add extra data to the rest-api response for this code.<br/>')

    def __str__(self) -> str:
        if self.department is not None:
            return f'{self.title}, {self.department.name}'
        return f'{self.title}'
