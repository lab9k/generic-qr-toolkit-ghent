from django.contrib.auth.decorators import login_required
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView

from . import views
from . import viewsets
from .schema import schema
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from graphene_django.views import GraphQLView
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()
router.register(r'qrcodes', viewsets.CodeViewSet, basename='api-code')
router.register(r'apihits', viewsets.ApiHitViewSet, basename='api-apihit')
router.register(r'departments', viewsets.DepartmentViewSet, basename='api-department')
router.register(r'urls', viewsets.LinkUrlViewSet, basename='api-url')

suffixed_urlpatterns = [
    # path('<uuid:uuid>/', views.QRCodeDetails.as_view(), name='qrcode-detail'),
    path('<slug:short_uuid>', views.QRCodeDetails.as_view(), name='qrcode-detail')
]
suffixed_urlpatterns = format_suffix_patterns(suffixed_urlpatterns, allowed=['html', 'json'])

urlpatterns = [
    path('code/<uuid>/', views.CodeView.as_view(), name='code-detail'),
    path('code/<uuid>/dl', views.download_code, name='code-dl'),
    path('code/generate/<int:amount>', views.generate, name='code-generate'),
]

urlpatterns += suffixed_urlpatterns

urlpatterns += [path('api/', include(router.urls)),
                # path('api/graphql/', login_required(GraphQLView.as_view(graphiql=True, schema=schema))),
                path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                path('openapi/', get_schema_view(
                    title="Qr code Toolkit API",
                    description="Stad Gent qr code toolkit",
                    version="1.0.0",
                    patterns=router.urls,
                    url='/api/'
                ), name='openapi-schema'),
                path('swagger-ui/', TemplateView.as_view(
                    template_name='api/swagger-ui.html',
                    extra_context={'schema_url': 'openapi-schema'}
                ), name='swagger-ui'),
                ]
