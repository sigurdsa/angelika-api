from test.testcase import AngelikaAPITestCase
from alarm.models import Alarm
from patient.models import Patient
from measurement.models import Measurement
from django.utils import timezone
from datetime import timedelta
from motivation_text.models import MotivationText


class PermissionTests(AngelikaAPITestCase):
    def test_alarm_list_unauthorized(self):
        response = self.client.get('/alarms/')
        self.assertEqual(response.status_code, 401)  # UNAUTHORIZED

    def test_alarm_list_as_health_professional(self):
        self.force_authenticate('helselise')

        first_patient = Patient.objects.first()
        measurement = Measurement.objects.create(
            type='O',
            value=90.5,
            patient=first_patient,
            time=timezone.now()
        )
        Alarm.objects.create(
            measurement=measurement,
            time_created=timezone.now()
        )

        response = self.client.get('/alarms/')
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response.data['count'], 1)
        self.assertTrue('results' in response.data)

    def test_patient_list_no_permission(self):
        self.force_authenticate('larsoverhaug')
        response = self.client.get('/alarms/')
        self.assertEqual(response.status_code, 403)  # PERMISSION DENIED


class GetTests(AngelikaAPITestCase):
    def test_list_unfiltered(self):
        self.force_authenticate('helselise')

        patient1 = Patient.objects.first()
        measurement1 = Measurement.objects.create(
            type='O',
            value=90.5,
            patient=patient1,
            time=timezone.now() - timedelta(days=1)
        )
        Alarm.objects.create(
            measurement=measurement1,
            time_created=timezone.now()
        )

        patient2 = self.create_patient('karinordmann', 'Kari', 'Nordmann', '02105534875')
        measurement2 = Measurement.objects.create(
            type='P',
            value=63,
            patient=patient2,
            time=timezone.now()
        )
        Alarm.objects.create(
            measurement=measurement2,
            time_created=timezone.now()
        )

        response = self.client.get('/alarms/')
        self.assertEqual(response.data['count'], 2)
        self.assertTrue('results' in response.data)
        alarms = response.data['results']
        alarm1 = alarms[0]
        self.assertEqual(alarm1['measurement']['type'], 'P')
        self.assertEqual(alarm1['measurement']['patient']['user']['full_name'], 'Kari Nordmann')

    def test_list_only_untreated(self):
        self.force_authenticate('helselise')

        patient1 = Patient.objects.first()
        measurement1 = Measurement.objects.create(
            type='O',
            value=90.5,
            patient=patient1,
            time=timezone.now() - timedelta(days=1)
        )
        Alarm.objects.create(
            measurement=measurement1,
            time_created=timezone.now(),
            is_treated=True
        )

        patient2 = self.create_patient('karinordmann', 'Kari', 'Nordmann', '02105534875')
        measurement2 = Measurement.objects.create(
            type='P',
            value=63,
            patient=patient2,
            time=timezone.now()
        )
        Alarm.objects.create(
            measurement=measurement2,
            time_created=timezone.now(),
            is_treated=False
        )

        response = self.client.get('/alarms/?only_untreated=1')
        self.assertEqual(response.data['count'], 1)
        self.assertTrue('results' in response.data)
        alarms = response.data['results']
        self.assertEqual(alarms[0]['measurement']['type'], 'P')

    def test_list_filtered_by_patient(self):
        self.force_authenticate('helselise')

        patient1 = Patient.objects.first()
        measurement1 = Measurement.objects.create(
            type='O',
            value=90.5,
            patient=patient1,
            time=timezone.now()
        )
        Alarm.objects.create(
            measurement=measurement1,
            time_created=timezone.now()
        )

        patient2 = self.create_patient('karinordmann', 'Kari', 'Nordmann', '02105534879')
        measurement2 = Measurement.objects.create(
            type='O',
            value=96.5,
            patient=patient2,
            time=timezone.now()
        )
        Alarm.objects.create(
            measurement=measurement2,
            time_created=timezone.now()
        )

        response = self.client.get('/alarms/?patient_id=' + str(patient1.id))
        self.assertEqual(response.data['count'], 1)
        self.assertTrue('results' in response.data)
        alarms = response.data['results']
        alarm1 = alarms[0]
        self.assertTrue('treated_text' in alarm1)
        self.assertAlmostEqual(alarm1['measurement']['value'], 90.5)
        self.assertFalse('patient' in alarm1['measurement'])

    def test_list_filtered_by_patient_parse_error(self):
        self.force_authenticate('helselise')
        response = self.client.get('/alarms/?patient_id=asd')
        self.assertEqual(response.status_code, 400)  # Bad request


class PostTests(AngelikaAPITestCase):
    def test_handle(self):
        patient1 = Patient.objects.first()
        measurement1 = Measurement.objects.create(
            type='O',
            value=96.5,
            patient=patient1,
            time=timezone.now()
        )
        alarm1 = Alarm.objects.create(
            measurement=measurement1,
            time_created=timezone.now()
        )

        self.force_authenticate('helselise')
        response = self.client.post(
            '/alarms/' + str(alarm1.id) + '/handle/',
            {
                'alarm': {
                    'is_treated': True,
                    'treated_text': 'Ensom',
                    'search_tag': 'Sorg',
                },
                'motivation_text': {
                    'text': 'Ta en kaffe med Ole-Petter'
                }
            },
            'json'
        )

        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response.data['alarm']['treated_text'], 'Ensom')
        self.assertEqual(response.data['alarm']['is_treated'], True)
        self.assertEqual(response.data['alarm']['search_tag'], 'Sorg')
        self.assertEqual(response.data['motivation_text']['text'], 'Ta en kaffe med Ole-Petter')
        self.assertTrue('id' in response.data['motivation_text'])
        self.assertEqual(MotivationText.objects.count(), 1)

    def test_handle_without_motivation_text(self):
        patient1 = Patient.objects.first()
        measurement1 = Measurement.objects.create(
            type='O',
            value=96.5,
            patient=patient1,
            time=timezone.now()
        )
        alarm1 = Alarm.objects.create(
            measurement=measurement1,
            time_created=timezone.now()
        )

        self.force_authenticate('helselise')
        response = self.client.post(
            '/alarms/' + str(alarm1.id) + '/handle/',
            {
                'alarm': {
                    'is_treated': True,
                    'treated_text': 'Ensom',
                    'search_tag': 'Sorg'
                },
                'motivation_text': {'text': ''}
            },
            'json'
        )

        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(MotivationText.objects.count(), 0)
        self.assertEqual(response.data['alarm']['search_tag'], 'Sorg')
