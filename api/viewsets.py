from api.serializers import QRCodeSerializer
from api.models import QRCode
from rest_framework import viewsets
from rest_framework import permissions


class CodeViewSet(viewsets.ModelViewSet):
    serializer_class = QRCodeSerializer
    queryset = QRCode.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
