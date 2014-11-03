from motivation_text.models import MotivationText
from patient.models import Patient
from test.testcase import AngelikaAPITestCase


class TestMotivation(AngelikaAPITestCase):
    def test_add_motivation_text(self):
        first_patient = Patient.objects.first()
        motivation_text = MotivationText(
            patient=first_patient,
            time_created='2014-10-24T09:46:20Z',
            text='HEI'
        )
        self.assertEqual(motivation_text.text, 'HEI')
    def test_current_information(self):
        self.force_authenticate('larsoverhaug')
        first_patient = Patient.objects.first()
        MotivationText.objects.create(
            patient=first_patient,
            text='HEI',
            time_created='2014-10-24T09:46:20Z',
            type='I'
        )
        response = self.client.get('/current-patient/')

        self.assertTrue('information_texts' in response.data)

    def test_current_motivation(self):
        self.force_authenticate('larsoverhaug')
        first_patient = Patient.objects.first()
        MotivationText.objects.create(
            patient=first_patient,
            text='HEI',
            time_created='2014-10-24T09:46:20Z',
            type='M'
        )
        response = self.client.get('/current-patient/')

        self.assertTrue('motivation_texts' in response.data)
