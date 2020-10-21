from api.serializers import QRCodeSerializer, ApiHitSerializer
from api.models import ApiHit, QRCode
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters


class CodeViewSet(viewsets.ModelViewSet):
    serializer_class = QRCodeSerializer
    queryset = QRCode.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]


class ApiHitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApiHitSerializer
    queryset = ApiHit.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('action',)
