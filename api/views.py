from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from .serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from api.models import QRCode
from api.serializers import QRCodeSerializer
from django.http import Http404
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class QRCodeList(APIView):
    def get(self, request, format=None):
        qrcodes = QRCode.objects.all()
        serializer = QRCodeSerializer(qrcodes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QRCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QRCodeDetails(APIView):

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get_object(self, pk):
        try:
            return QRCode.objects.get(pk=pk)
        except QRCode.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        qrcode = self.get_object(pk)
        serializer = QRCodeSerializer(qrcode)
        return Response(serializer.data)





    def put(self, request, pk, format=None):
        qrcode = self.get_object(pk)
        serializer = QRCodeSerializer(qrcode, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        qrcode = self.get_object(pk)
        qrcode.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
