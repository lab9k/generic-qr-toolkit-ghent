from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin
from api.models import Department, LinkUrl, QRCode, ApiHit


class DepartmentSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['name']


class LinkUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkUrl
        exclude = ['id', 'code']


class QRCodeSerializer(WritableNestedModelSerializer):
    department = DepartmentSerializer()
    urls = LinkUrlSerializer(many=True)

    class Meta:
        model = QRCode
        fields = '__all__'
        read_only_fields = ['created', 'last_updated']


class ApiHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiHit
        fields = '__all__'
