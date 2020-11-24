from django.urls import reverse
from django.views.generic.list import ListView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from api.models import ApiHit, QRCode
from api.serializers import QRCodeSerializer
from django.http import Http404, HttpResponseForbidden, HttpResponse
from rest_framework.views import APIView
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.views.generic import DetailView, ListView
import requests


class CodeList(ListView):
    template_name = 'api/qrcode/code_list.html'
    queryset = QRCode.objects.all()
    context_object_name = 'codes'


def download_code(request, uuid):
    code = get_object_or_404(QRCode, uuid=uuid)
    code_url = request.build_absolute_uri(reverse("qrcode-detail", kwargs=dict(uuid=code.uuid)))
    image_url = f'http://qrcodeservice.herokuapp.com/?query={code_url}'
    image_resp = requests.get(image_url).text

    response = HttpResponse(image_resp, content_type='image/svg+xml')
    response['Content-Length'] = len(response.content)
    response['Content-Disposition'] = f'attachment; filename="{code.title}.svg"'
    return response


class CodeView(DetailView):
    template_name = 'api/qrcode/code.html'
    pk_url_kwarg = 'uuid'
    queryset = QRCode.objects.all()
    context_object_name = 'code'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get(self.pk_url_kwarg)
        try:
            return self.queryset.get(uuid=uuid)
        except QRCode.DoesNotExist or ValidationError:
            raise Http404


class QRCodeDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    permission_classes = []

    @staticmethod
    def get_object(uuid):
        try:
            return QRCode.objects.get(uuid=uuid)
        except QRCode.DoesNotExist or ValidationError:
            raise Http404

    def get(self, request, uuid, format=None):
        qrcode = self.get_object(uuid)

        if request.accepted_renderer.format == 'json' or format == 'json':
            if request.user.is_authenticated:
                hit = ApiHit(
                    code=qrcode, action='json')
                hit.save()
                serializer = QRCodeSerializer(qrcode)
                return Response(serializer.data)
            else:
                raise NotAuthenticated

        if request.accepted_renderer.format == 'html' or format == 'html':
            if qrcode.urls.count() == 0:
                hit = ApiHit(code=qrcode, action=ApiHit.ACTION_CHOICES.HTML)
                hit.save()
                return Response({'qrcode': qrcode}, template_name='api/index.html')

            if qrcode.mode == QRCode.REDIRECT_MODE_CHOICES.REDIRECT:
                hit = ApiHit(
                    code=qrcode, action=ApiHit.ACTION_CHOICES.REDIRECT)
                hit.save()
                return redirect(qrcode.urls.first().url, permanent=False)
            if qrcode.mode == QRCode.REDIRECT_MODE_CHOICES.KIOSK:
                hit = ApiHit(code=qrcode, action=ApiHit.ACTION_CHOICES.HTML)
                hit.save()
                return Response({'qrcode': qrcode}, template_name='api/kiosk.html')
            if qrcode.mode == QRCode.REDIRECT_MODE_CHOICES.INFO_PAGE:
                hit = ApiHit(code=qrcode, action=ApiHit.ACTION_CHOICES.HTML)
                hit.save()
                return Response({'qrcode': qrcode}, template_name='api/index.html')

            return Response({'qrcode': qrcode}, template_name='api/index.html')

        hit = ApiHit(
            code=qrcode, action='json')
        hit.save()
        serializer = QRCodeSerializer(qrcode)
        return Response(serializer.data)
