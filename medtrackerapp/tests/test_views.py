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
        self.url = reverse("expected-doses", args=[self.med.id])

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

    def test_expected_doses_valid_request(self):
        """Test successful request with valid days parameter."""
        response = self.client.get(self.url, {"days": 7})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["medication_id"], self.med.id)
        self.assertEqual(response.data["days"], 7)
        self.assertEqual(response.data["expected_doses"], 14)  # 7 days * 2 per day

    def test_expected_doses_missing_days_parameter(self):
        """Test request without days parameter returns 400."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_expected_doses_negative_days(self):
        """Test request with negative days returns 400."""
        response = self.client.get(self.url, {"days": -5})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_expected_doses_non_integer_days(self):
        """Test request with non-integer days returns 400."""
        response = self.client.get(self.url, {"days": "abc"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_expected_doses_float_days(self):
        """Test request with float days returns 400."""
        response = self.client.get(self.url, {"days": "3.5"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_expected_doses_zero_days(self):
        """Test request with zero days returns valid response."""
        response = self.client.get(self.url, {"days": 0})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["days"], 0)
        self.assertEqual(response.data["expected_doses"], 0)

    def test_expected_doses_invalid_medication_id(self):
        """Test request with non-existent medication returns 404."""
        invalid_url = reverse("expected-doses", args=[9999])
        response = self.client.get(invalid_url, {"days": 7})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Medication, 'expected_doses')
    def test_expected_doses_value_error_from_model(self, mock_expected_doses):
        """Test that ValueError from model method returns 400."""
        mock_expected_doses.side_effect = ValueError("Days and schedule must be positive.")

        response = self.client.get(self.url, {"days": 5})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_expected_doses_large_number_of_days(self):
        """Test request with large number of days."""
        response = self.client.get(self.url, {"days": 365})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["days"], 365)
        self.assertEqual(response.data["expected_doses"], 730)