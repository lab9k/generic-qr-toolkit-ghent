from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase

from api.models import Department
from api.viewsets import CodeViewSet

User = get_user_model()


class ApiTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        department = Department(name='Test Department')
        department.save()
        self.user = User.objects.create_user(username='tester', email='email123@gmail.com', password='blabla12345',
                                             department=department)

    def test_details(self):
        request = self.factory.get('/api/qrcodes', format='json')

        request.user = self.user

        viewset = CodeViewSet.as_view({'get': 'list'})
        response = viewset(request)
        self.assertEquals(response.status_code, 200)
