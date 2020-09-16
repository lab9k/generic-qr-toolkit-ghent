# Generated by Django 3.1.1 on 2020-09-15 09:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('form_url', models.URLField(blank=True, default='', help_text='links to a form')),
                ('redirect_url', models.URLField(blank=True, default='', help_text='redirect to external page')),
                ('basic_info', models.CharField(help_text='short information about device', max_length=1000)),
            ],
        ),
    ]
