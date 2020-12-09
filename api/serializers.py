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
        fields = '__all__'


class QRCodeSerializer(serializers.ModelSerializer):
    urls = LinkUrlSerializer(many=True, read_only=True)
    department = DepartmentSerializer()

    def create(self, validated_data):
        validated_dept = validated_data.pop('department')
        dept, created = Department.objects.get_or_create(name=validated_dept['name'])
        code = QRCode.objects.create(**validated_data, department=dept)
        return code

    class Meta:
        model = QRCode
        fields = '__all__'
        read_only_fields = ['created', 'last_updated']


class ApiHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiHit
        fields = '__all__'
