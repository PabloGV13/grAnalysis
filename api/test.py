from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Stay
from .serializers import StaySerializer

class GetAllStaysTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.stay1 = Stay.objects.create(name="Stay 1", url="http://example.com/1", location="Location 1", is_analysed=True)
        self.stay2 = Stay.objects.create(name="Stay 2", url="http://example.com/2", location="Location 2", is_analysed=True)
        self.stay3 = Stay.objects.create(name="Stay 3", url="http://example.com/3", location="Location 3", is_analysed=False)  # Este no debería ser incluido

    def test_get_all_stays(self):
        response = self.client.get(reverse('get-all-stays'))  
        stays = Stay.objects.filter(is_analysed=True)
        serializer = StaySerializer(stays, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class GetStayTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Crear objetos Stay para usar en las pruebas
        self.stay1 = Stay.objects.create(name="Stay 1", url="http://example.com/1", location="Location 1", is_analysed=True)
        self.stay2 = Stay.objects.create(name="Stay 2", url="http://example.com/2", location="Location 2", is_analysed=True)

    def test_get_valid_stay(self):
        response = self.client.get(reverse('get-stay', kwargs={'id': self.stay1.stay_id}))
        stay = Stay.objects.get(stay_id=self.stay1.stay_id)
        serializer = StaySerializer(stay)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_stay(self):
        response = self.client.get(reverse('get-stay', kwargs={'id': 9999}))  # ID que no existe
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        

