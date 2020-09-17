from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('qrcodes/', views.QRCodeList.as_view()),
    path('qrcodes/<pk>/', views.QRCodeDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
