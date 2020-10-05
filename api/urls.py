from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('code/', views.QRCodeList.as_view()),
    path('qrcodes/<int:n>', views.QRCodeBulkCreate.as_view()),
    path('<uuid>/', views.QRCodeDetails.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
