from rest_framework import serializers
from api.models import Department, QRCode


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']


class QRCodeSerializer(serializers.ModelSerializer):

    department = DepartmentSerializer()

    class Meta:
        model = QRCode
        fields = ['id', 'title', 'form_url',
                  'redirect_url', 'basic_info', 'uuid', 'department']
