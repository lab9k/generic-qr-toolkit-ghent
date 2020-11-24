from rest_framework import serializers
from api.models import Department, LinkUrl, QRCode, ApiHit


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['name']


class LinkUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkUrl
        exclude = ['code']


class QRCodeSerializer(serializers.ModelSerializer):
    urls = LinkUrlSerializer(many=True)

    class Meta:
        model = QRCode
        fields = '__all__'
        read_only_fields = ['created', 'last_updated', 'urls']

    def create(self, validated_data):
        link_urls = validated_data.pop('urls')
        code = super(QRCodeSerializer, self).create(validated_data)
        for url in link_urls:
            LinkUrl.objects.create(code=code, **url)
        return code

    def update(self, instance, validated_data):
        link_urls = validated_data.pop('urls')
        code = super(QRCodeSerializer, self).update(instance, validated_data)
        for url in link_urls:
            LinkUrl.objects.get_or_create(code=code, **url)
        return code


class ApiHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiHit
        fields = '__all__'
