from rest_framework.test import APITestCase
from medtrackerapp.models import Medication
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, Mock
from rest_framework.test import APITestCase
from medtrackerapp.models import Medication
from django.urls import reverse
from rest_framework import status

class MedicationViewTests(APITestCase):
    def setUp(self):
        self.med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=2)

    def test_list_medications_valid_data(self):
        url = reverse("medication-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Aspirin")
        self.assertEqual(response.data[0]["dosage_mg"], 100)

        self.assertEqual(len(response.data), 1)
    def test_retrieve_medication_valid_id(self):
        url = reverse("medication-detail", args=[self.med.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Aspirin")
        self.assertEqual(response.data["dosage_mg"], 100)
    def test_retrieve_medication_invalid_id(self):
        url = reverse("medication-detail", args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_list_medications_valid_data(self):
        url = reverse("medication-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Aspirin")
        self.assertEqual(response.data[0]["dosage_mg"], 100)

        self.assertEqual(len(response.data), 1)

    def test_retrieve_medication_valid_id(self):
        url = reverse("medication-detail", args=[self.med.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Aspirin")
        self.assertEqual(response.data["dosage_mg"], 100)

    def test_retrieve_medication_invalid_id(self):
        url = reverse("medication-detail", args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('medtrackerapp.services.DrugInfoService.get_drug_info')
    def test_drug_info_api_mocked(self, mock_get_drug_info):

        mock_response = {
            'name': 'Aspirin',
            'dosage_mg': 100,
            'prescribed_per_day': 2
        }
        mock_get_drug_info.return_value = mock_response

        url = reverse("medication-detail", kwargs={'pk': self.med.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Aspirin')

