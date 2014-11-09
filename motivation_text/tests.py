from motivation_text.models import MotivationText
from patient.models import Patient
from test.testcase import AngelikaAPITestCase
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class TestMotivation(AngelikaAPITestCase):
    def test_add_motivation_text(self):
        first_patient = Patient.objects.first()
        motivation_text = MotivationText(
            patient=first_patient,
            text='HEI'
        )
        self.assertEqual(motivation_text.text, 'HEI')

    def test_current_information(self):
        self.force_authenticate('larsoverhaug')
        first_patient = Patient.objects.first()
        MotivationText.objects.create(
            patient=first_patient,
            text='HEI',
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
            type='M'
        )
        response = self.client.get('/current-patient/')

        self.assertTrue('motivation_texts' in response.data)


class TestCronjobs(AngelikaAPITestCase):
    def test_delete_old_motivation_texts(self):
        first_patient = Patient.objects.first()
        text = MotivationText.objects.create(
            patient=first_patient,
            text='Alle liker deg',
            type='M'
        )
        text.time_created = timezone.now() - timedelta(days=40)
        text.save()
        MotivationText.objects.create(
            patient=first_patient,
            text='Jakka di er jammen fin!',
            type='M'
        )
        MotivationText.objects.create(
            patient=first_patient,
            text='Fisk er sunt!',
            type='I'
        )

        response = self.client.post('/motivation_texts/delete_old/?cron_key=' + settings.CRON_KEY)
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response.data['num_deleted_rows'], 1)
        self.assertEqual(MotivationText.objects.count(), 2)
