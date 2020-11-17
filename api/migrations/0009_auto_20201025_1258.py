# Generated by Django 3.1.2 on 2020-10-25 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_qrcode_extra_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='extra_data',
            field=models.JSONField(blank=True, default=dict, help_text='Use this to add extra data to the rest-api response for this code.<br/>'),
        ),
    ]