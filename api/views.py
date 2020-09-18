from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from api.models import QRCode
from api.serializers import QRCodeSerializer
from django.http import Http404
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.core.exceptions import ValidationError


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


class QRCodeBulkCreate(APIView):
    renderer_classes = [JSONRenderer]

    @staticmethod
    def post(request, n, format=None):
        """ create n new empty models and return the uuids """
        uuids = []
        for i in range(n):
            qrcode = QRCode()
            if request is not {}:
                serializer = QRCodeSerializer(qrcode, data=request.data)
            else:
                serializer = QRCodeSerializer(qrcode, data={"title": "generated with batch number: " + str(i)})
            if serializer.is_valid():
                serializer.save()
                uuids.append(serializer.data['id'])
        return Response(uuids)


class QRCodeDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    @staticmethod
    def get_object(pk):
        try:
            return QRCode.objects.get(pk=pk)
        except QRCode.DoesNotExist or ValidationError:
            raise Http404

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

    def put(self, request, pk, format=None):
        if QRCode.objects.filter(pk=pk).exists():
            qrcode = self.get_object(pk)
        else:
            qrcode = QRCode(request.data)
        serializer = QRCodeSerializer(qrcode, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'qrcode': serializer.data}, template_name='index.html')
        raise Http404
