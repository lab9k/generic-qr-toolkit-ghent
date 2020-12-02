from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from api.models import ApiHit, QRCode
from api.serializers import QRCodeSerializer
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.views.generic import DetailView, ListView
import requests
import io
import zipfile
from uuid import uuid4


class CodeList(ListView):
    template_name = 'api/qrcode/code_list.html'
    queryset = QRCode.objects.all()
    context_object_name = 'codes'


def download_code(request, uuid):
    if request.user.is_authenticated:
        code, created = QRCode.objects.get_or_create(uuid=uuid, defaults={'department': request.user.department})
        if created:
            code.title = request.GET.get('title', 'Auto Generated Code')
            code.save()
    else:
        code = QRCode.objects.get(uuid=uuid)
    code_url = request.build_absolute_uri(reverse("qrcode-detail", kwargs=dict(uuid=code.uuid)))
    image_url = f'http://qrcodeservice.herokuapp.com/?query={code_url}'
    image_resp = requests.get(image_url).text

    response = HttpResponse(image_resp, content_type='image/svg+xml')
    response['Content-Length'] = len(response.content)
    response['Content-Disposition'] = f'attachment; filename="{code.title}.svg"'
    return response


@login_required
def generate(request, amount):
    zip_filename = 'generated_codes.zip'
    s = io.BytesIO()

    zf = zipfile.ZipFile(s, mode='w', compression=zipfile.ZIP_DEFLATED)
    uuids = [uuid4() for x in range(amount)]

    for uuid in uuids:
        code_url = request.build_absolute_uri(reverse('qrcode-detail', kwargs=dict(uuid=uuid)))
        image_url = f'http://qrcodeservice.herokuapp.com/?query={code_url}'
        res = requests.get(image_url)
        zf.writestr(f'Auto Generated Code-{uuid}.svg', res.content)

    zf.close()

    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    resp['Content-Disposition'] = f'attachment; filename={zip_filename}'
    return resp


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
                    code=qrcode, action=ApiHit.ACTION_CHOICES.JSON)
                hit.save()
                serializer = QRCodeSerializer(qrcode)
                return Response(serializer.data)
            else:
                raise NotAuthenticated

        if request.accepted_renderer.format == 'html' or format == 'html':
            if qrcode.urls.count() == 0:
                hit = ApiHit(code=qrcode, action=ApiHit.ACTION_CHOICES.BASIC_INFO)
                hit.save()
                return Response({'qrcode': qrcode}, template_name='api/qrcode/index.html')

            if qrcode.mode == QRCode.REDIRECT_MODE_CHOICES.REDIRECT:
                hit = ApiHit(
                    code=qrcode, action=ApiHit.ACTION_CHOICES.REDIRECT)
                hit.save()
                return redirect(qrcode.urls.first().url, permanent=False)
            if qrcode.mode == QRCode.REDIRECT_MODE_CHOICES.KIOSK:
                hit = ApiHit(code=qrcode, action=ApiHit.ACTION_CHOICES.KIOSK)
                hit.save()
                return Response({'qrcode': qrcode}, template_name='api/qrcode/kiosk.html')
            if qrcode.mode == QRCode.REDIRECT_MODE_CHOICES.INFO_PAGE:
                hit = ApiHit(code=qrcode, action=ApiHit.ACTION_CHOICES.BASIC_INFO)
                hit.save()
                return Response({'qrcode': qrcode}, template_name='api/qrcode/index.html')

            return Response({'qrcode': qrcode}, template_name='api/qrcode/index.html')

        hit = ApiHit(
            code=qrcode, action=ApiHit.ACTION_CHOICES.JSON)
        hit.save()
        serializer = QRCodeSerializer(qrcode)
        return Response(serializer.data)
