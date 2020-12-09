from rest_framework import serializers
from api.models import Department, LinkUrl, QRCode, ApiHit


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class LinkUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkUrl
        fields = '__all__'


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'
        read_only_fields = ['created', 'last_updated']


class ApiHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiHit
        fields = '__all__'
