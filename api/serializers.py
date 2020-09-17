from rest_framework import serializers
from api.models import QRCode


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id', 'title', 'form_url', 'redirect_url', 'basic_info', ]
