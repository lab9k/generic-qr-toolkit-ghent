from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('code/', views.CodeList.as_view()),
    path('code/<uuid>/', views.CodeView.as_view()),
    path('qrcodes/', views.QRCodeList.as_view()),
    path('qrcodes/<int:n>', views.QRCodeBulkCreate.as_view()),
    path('<uuid:uuid>/', views.QRCodeDetails.as_view(), name='qrcode-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
