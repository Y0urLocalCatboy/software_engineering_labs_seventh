from django.test import TestCase
from medtrackerapp.models import Medication, DoseLog
from django.utils import timezone
from datetime import timedelta


class MedicationModelTests(TestCase):

    def test_str_returns_name_and_dosage(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=2)
        self.assertEqual(str(med), "Aspirin (100mg)")

    def test_adherence_rate_all_doses_taken(self):
        med = Medication.objects.create(name="Aspirin", dosage_mg=100, prescribed_per_day=2)

        now = timezone.now()
        DoseLog.objects.create(medication=med, taken_at=now - timedelta(hours=30))
        DoseLog.objects.create(medication=med, taken_at=now - timedelta(hours=1))

        adherence = med.adherence_rate()
        self.assertEqual(adherence, 100.0)
    def test_valid_medication_creation(self):
        med = Medication.objects.create(name="Ibuprofen", dosage_mg=200, prescribed_per_day=3)
        self.assertIsInstance(med, Medication)
        self.assertEqual(med.name, "Ibuprofen")
        self.assertEqual(med.dosage_mg, 200)
        self.assertEqual(med.prescribed_per_day, 3)
    def test_expected_doses_calculation(self):
        med = Medication.objects.create(name="Paracetamol", dosage_mg=500, prescribed_per_day=4)
        expected_doses = med.expected_doses(7)
        self.assertEqual(expected_doses, 28)
    def test_expected_doses_invalid_days(self):
        med = Medication.objects.create(name="Paracetamol", dosage_mg=500, prescribed_per_day=4)
        with self.assertRaises(ValueError):
            med.expected_doses(-5)
