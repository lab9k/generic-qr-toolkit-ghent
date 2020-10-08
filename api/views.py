from django.views.generic.list import ListView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST
from api.models import ApiHit, QRCode
from api.serializers import QRCodeSerializer
from django.http import Http404
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.views.generic import DetailView, ListView


class CodeList(ListView):
    template_name = 'code_list.html'
    queryset = QRCode.objects.all()
    context_object_name = 'codes'


class CodeView(DetailView):
    template_name = 'code.html'
    pk_url_kwarg = 'uuid'
    queryset = QRCode.objects.all()
    context_object_name = 'code'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get(self.pk_url_kwarg)
        try:
            return self.queryset.get(uuid=uuid)
        except QRCode.DoesNotExist or ValidationError:
            raise Http404


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
                serializer = QRCodeSerializer(
                    qrcode, data={"title": f"generated with batch number: {str(i)}"})
            if serializer.is_valid():
                serializer.save()
                uuids.append(serializer.data['id'])
            else:
                Response(serializer.errors,
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(uuids)


class QRCodeDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    @staticmethod
    def get_object(uuid):
        try:
            return QRCode.objects.get(uuid=uuid)
        except QRCode.DoesNotExist or ValidationError:
            raise Http404

    def get(self, request, uuid, format=None):
        qrcode = self.get_object(uuid)

        if request.accepted_renderer.format == 'json' or format == 'json':
            hit = ApiHit(
                code=qrcode, action='json')
            hit.save()
            serializer = QRCodeSerializer(qrcode)
            return Response(serializer.data)
        """ When both form url and basic info aren't just redirect to redirect url """
        if qrcode.form_url == '' and qrcode.basic_info == '' and qrcode.redirect_url != '':
            hit = ApiHit(
                code=qrcode, action='redirect')
            hit.save()
            return redirect(qrcode.redirect_url)

        if request.accepted_renderer.format == 'html' or format == 'html':
            hit = ApiHit(
                code=qrcode, action='basic_info')
            hit.save()
            return Response({'qrcode': qrcode}, template_name='index.html')

        hit = ApiHit(
            code=qrcode, action='json')
        hit.save()
        serializer = QRCodeSerializer(qrcode)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        if QRCode.objects.filter(uuid=uuid).exists():
            qrcode = self.get_object(uuid)
        else:
            qrcode = QRCode(request.data)
        serializer = QRCodeSerializer(qrcode, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'qrcode': serializer.data}, template_name='index.html')
        raise HTTP_400_BAD_REQUEST
