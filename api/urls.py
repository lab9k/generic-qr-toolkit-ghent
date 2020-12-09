from django.urls import path
from django.urls.conf import include
from api import views
from api import viewsets
from api.schema import schema
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from graphene_django.views import GraphQLView

router = routers.DefaultRouter()
router.register(r'qrcodes', viewsets.CodeViewSet)
router.register(r'apihits', viewsets.ApiHitViewSet)
router.register(r'departments', viewsets.DepartmentViewSet)

urlpatterns = [
    path('code/', views.CodeList.as_view()),
    path('code/<uuid>/', views.CodeView.as_view(), name='code-detail'),
    path('code/<uuid>/dl', views.download_code, name='code-dl'),
    path('code/generate/<int:amount>', views.generate, name='code-generate'),
    path('<uuid:uuid>/', views.QRCodeDetails.as_view(), name='qrcode-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
urlpatterns += [path('api/rest/', include(router.urls)),
                path('api/graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
                path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), ]
