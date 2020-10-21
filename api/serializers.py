from rest_framework import serializers
from api.models import Department, LinkUrl, QRCode, ApiHit


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']


class LinkUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkUrl
        exclude = ['id', 'code']


class QRCodeSerializer(serializers.ModelSerializer):

    department = DepartmentSerializer()
    urls = LinkUrlSerializer(many=True)

    class Meta:
        model = QRCode
        exclude = ['id']
        read_only_fields = ['created', 'last_updated']


class ApiHitSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiHit
        fields = '__all__'
