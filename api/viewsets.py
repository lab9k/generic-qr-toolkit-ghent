from api.serializers import QRCodeSerializer, ApiHitSerializer
from api.models import ApiHit, QRCode
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend


class CodeViewSet(viewsets.ModelViewSet):
    serializer_class = QRCodeSerializer
    queryset = QRCode.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('mode', 'title', 'created', 'last_updated', 'uuid')


class ApiHitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApiHitSerializer
    queryset = ApiHit.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('action', 'hit_date', 'code')
