# Generated by Django 3.1.2 on 2020-10-25 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20201008_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrcode',
            name='extra_data',
            field=models.JSONField(default=dict, help_text='Use this to add extra data to the rest-api response for this code.<br/>'),
        ),
    ]
