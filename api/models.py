from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class ApiHit(models.Model):
    class ACTION_CHOICES(models.TextChoices):
        BASIC_INFO = 'basic_info', _('Basic info')
        JSON = 'json', _('Json Response')
        REDIRECT = 'redirect', _('Redirect')

    hit_date = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=256, default='')
    action = models.CharField(
        max_length=16, choices=ACTION_CHOICES.choices, default=ACTION_CHOICES.BASIC_INFO)
    code = models.ForeignKey(
        'QRCode', on_delete=models.CASCADE, related_name='hits')


class Department(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.name}'


class QRCode(models.Model):
    title = models.CharField(blank=True, default='', max_length=100)
    department = models.ForeignKey(
        to=Department, on_delete=models.SET_NULL, null=True)

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=True
    )

    form_url = models.URLField(
        blank=True, default='', help_text='links to a form')
    redirect_url = models.URLField(
        blank=True, default='', help_text='redirect to external page')
    basic_info = models.TextField(blank=True, default='')

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if self.department is not None:
            return f'{self.title}, {self.department.name}'
        return f'{self.title}'
