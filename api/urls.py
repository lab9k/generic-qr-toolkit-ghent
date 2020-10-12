from django.urls import path
from django.urls.conf import include
from api import views
from api import viewsets
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'qrcodes', viewsets.CodeViewSet)

urlpatterns = [
    path('code/', views.CodeList.as_view()),
    path('code/<uuid>/', views.CodeView.as_view()),
    path('<uuid:uuid>/', views.QRCodeDetails.as_view(), name='qrcode-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
urlpatterns += [path('api/', include(router.urls))]
