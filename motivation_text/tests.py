from django.test import TestCase
from motivation_text.models import MotivationText
from patient.models import Patient
from test.testcase import AngelikaAPITestCase


class TestMotivation(AngelikaAPITestCase):
    def test_add_motivation_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.all().first()
        motivation_text = MotivationText(
            patient=first_patient,
            time_created='2014-10-24T09:46:20Z',
            text='HEI'
        )
        self.assertEqual(motivation_text.text, 'HEI')
