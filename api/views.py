from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from api.models import QRCode
from api.serializers import QRCodeSerializer
from django.http import Http404
from rest_framework.views import APIView
from django.shortcuts import redirect


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

    @staticmethod
    def get_object(pk):
        try:
            return QRCode.objects.get(pk=pk)
        except QRCode.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        qrcode = self.get_object(pk)
        """ When both form url and basic info aren't just redirect to redirect url """
        if qrcode.form_url == '' and qrcode.basic_info == '':
            return redirect(qrcode.redirect_url)

        if request.accepted_renderer.format == 'html' or format == 'html':
            return Response({'qrcode': qrcode}, template_name='index.html')
        else:
            serializer = QRCodeSerializer(qrcode)
            return Response(serializer.data)
