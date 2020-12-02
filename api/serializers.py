from rest_framework import serializers
from api.models import Department, LinkUrl, QRCode, ApiHit


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []},
        }


class LinkUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkUrl
        exclude = ['code', 'id']


class QRCodeSerializer(serializers.ModelSerializer):
    urls = LinkUrlSerializer(many=True)
    department = DepartmentSerializer(required=True)

    def create(self, validated_data):
        urls_data = validated_data.pop('urls')
        dep_data = validated_data.pop('department')
        department, created = Department.objects.get_or_create(**dep_data)
        code = QRCode.objects.create(**validated_data, department=department)
        for url in urls_data:
            LinkUrl.objects.create(code=code, **url)
        return code

    def update(self, instance, validated_data):
        urls_data = validated_data.pop('urls')
        dep_data = validated_data.pop('department')
        department, created = Department.objects.get_or_create(**dep_data)
        instance.department = department
        # TODO: This can be cleaner
        LinkUrl.objects.filter(code=instance).delete()
        for url in urls_data:
            LinkUrl.objects.create(code=instance, **url)
        return instance

    class Meta:
        model = QRCode
        fields = '__all__'
        read_only_fields = ['created', 'last_updated']


class ApiHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiHit
        fields = '__all__'
