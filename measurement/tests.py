from test.testcase import AngelikaAPITestCase
from patient.models import Patient
from measurement.models import Measurement
from threshold_value.models import ThresholdValue
from pytz import UTC
from datetime import datetime
from alarm.models import Alarm
import time


class PostMeasurementTests(AngelikaAPITestCase):
    def test_post_ignored_measurements(self):
        hub_user = self.create_hub('hub1')
        larsoverhaug = Patient.objects.get(user__username='larsoverhaug')
        larsoverhaug.hub = hub_user
        larsoverhaug.save()
        self.force_authenticate('hub1')

        data = {
            "Measurements": [
                {
                    "date": 1414972800,
                    "type": "distance",
                    "unit": "m",
                    "value": 962.26
                },
                {
                    "date": 1414972800,
                    "type": "calories",
                    "unit": "kcal",
                    "value": 48.92
                },
                {
                    "date": 1414972800,
                    "type": "steps",
                    "unit": "steps",
                    "value": 1067
                }
            ],
            "Observation": {
                "hub_id": "hub1"
            }
        }

        self.assertEqual(Measurement.objects.count(), 0)  # Nothing is created yet

        response = self.client.post('/post-measurements/', data, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(response.data["num_measurements_created"], 1)  # One object created
        self.assertEqual(Measurement.objects.count(), 1)  # One object created
        self.assertAlmostEqual(Measurement.objects.first().value, 1067.0)  # Correct no of steps
        self.assertEqual(Measurement.objects.first().patient, larsoverhaug)  # Correct patient
        self.assertEqual(Alarm.objects.count(), 0)

    def test_post_when_not_authenticated(self):
        response = self.client.post('/post-measurements/', {}, 'json')
        self.assertEqual(response.status_code, 401)

    def test_post_bad_hub_id(self):
        hub_user = self.create_hub('hub1')
        larsoverhaug = Patient.objects.get(user__username='larsoverhaug')
        larsoverhaug.hub = hub_user
        larsoverhaug.save()
        self.force_authenticate('hub1')

        data = {
            "Measurements": [
                {
                    "date": 1414972800,
                    "type": "steps",
                    "unit": "steps",
                    "value": 1067
                }
            ],
            "Observation": {
                "hub_id": "dsfkjhdsfkjhdsf"
            }
        }
        response = self.client.post('/post-measurements/', data, 'json')
        self.assertEqual(response.status_code, 400)

    def test_post_abnormal_low_measurements(self):
        hub_user = self.create_hub('hub1')
        larsoverhaug = Patient.objects.get(user__username='larsoverhaug')
        larsoverhaug.hub = hub_user
        larsoverhaug.save()
        self.force_authenticate('hub1')

        lower_threshold_value = ThresholdValue.objects.create(
            value=49,
            patient=larsoverhaug,
            type='P',
            is_upper_threshold=False,
        )
        upper_threshold_value = ThresholdValue.objects.create(
            value=165,
            patient=larsoverhaug,
            type='P',
            is_upper_threshold=False,
        )

        measurement_time = int(time.time()) + 10000
        data = {
            "Measurements": [
                {
                    "date": measurement_time,
                    "type": "heart_rate",
                    "unit": "bpm",
                    "value": 42
                }
            ],
            "Observation": {
                "hub_id": "hub1"
            }
        }

        response = self.client.post('/post-measurements/', data, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Measurement.objects.count(), 1)
        self.assertEqual(Alarm.objects.count(), 1)
        self.assertEqual(Alarm.objects.first().measurement.pk, Measurement.objects.first().pk)

    def test_post_abnormal_high_measurements(self):
        hub_user = self.create_hub('hub1')
        larsoverhaug = Patient.objects.get(user__username='larsoverhaug')
        larsoverhaug.hub = hub_user
        larsoverhaug.save()
        self.force_authenticate('hub1')

        ThresholdValue.objects.create(
            value=49,
            patient=larsoverhaug,
            type='P',
            is_upper_threshold=False,
        )
        ThresholdValue.objects.create(
            value=165,
            patient=larsoverhaug,
            type='P',
            is_upper_threshold=False,
        )

        measurement_time = int(time.time()) + 10000
        data = {
            "Measurements": [
                {
                    "date": measurement_time,
                    "type": "heart_rate",
                    "unit": "bpm",
                    "value": 180
                }
            ],
            "Observation": {
                "hub_id": "hub1"
            }
        }

        response = self.client.post('/post-measurements/', data, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Measurement.objects.count(), 1)
        self.assertEqual(Alarm.objects.count(), 1)
        self.assertEqual(Alarm.objects.first().measurement.pk, Measurement.objects.first().pk)

    def test_post_abnormal_low_measurements_repeatedly(self):
        hub_user = self.create_hub('hub1')
        larsoverhaug = Patient.objects.get(user__username='larsoverhaug')
        larsoverhaug.hub = hub_user
        larsoverhaug.save()
        self.force_authenticate('hub1')

        lower_threshold_value = ThresholdValue.objects.create(
            value=49,
            patient=larsoverhaug,
            type='P',
            is_upper_threshold=False,
        )
        upper_threshold_value = ThresholdValue.objects.create(
            value=165,
            patient=larsoverhaug,
            type='P',
            is_upper_threshold=False,
        )

        measurement_time = int(time.time()) + 10000
        data = {
            "Measurements": [
                {
                    "date": measurement_time,
                    "type": "heart_rate",
                    "unit": "bpm",
                    "value": 42
                }
            ],
            "Observation": {
                "hub_id": "hub1"
            }
        }

        response = self.client.post('/post-measurements/', data, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Measurement.objects.count(), 1)
        self.assertEqual(Alarm.objects.count(), 1)

        data = {
            "Measurements": [
                {
                    "date": measurement_time + 500,
                    "type": "heart_rate",
                    "unit": "bpm",
                    "value": 41
                }
            ],
            "Observation": {
                "hub_id": "hub1"
            }
        }

        response = self.client.post('/post-measurements/', data, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Measurement.objects.count(), 2)
        self.assertEqual(Alarm.objects.count(), 1)  # no new alarm has been created

    def test_post_abnormal_low_measurements_multiple_patients(self):
        hub_user1 = self.create_hub('hub1')
        larsoverhaug = Patient.objects.get(user__username='larsoverhaug')
        larsoverhaug.hub = hub_user1
        larsoverhaug.save()

        hub_user2 = self.create_hub('hub2')
        kristin = self.create_patient('kristin', 'Kristin Hegine', 'Taraldsen')
        kristin.hub = hub_user2
        kristin.save()

        self.force_authenticate('hub1')

        ThresholdValue.objects.create(
            value=49,
            patient=larsoverhaug,
            type='P',
            is_upper_threshold=False,
        )
        ThresholdValue.objects.create(
            value=165,
            patient=larsoverhaug,
            type='P',
            is_upper_threshold=False,
        )

        ThresholdValue.objects.create(
            value=46,
            patient=kristin,
            type='P',
            is_upper_threshold=False,
        )
        ThresholdValue.objects.create(
            value=160,
            patient=kristin,
            type='P',
            is_upper_threshold=False,
        )

        measurement_time = int(time.time()) + 10000
        data1 = {
            "Measurements": [
                {
                    "date": measurement_time,
                    "type": "heart_rate",
                    "unit": "bpm",
                    "value": 42
                }
            ],
            "Observation": {
                "hub_id": "hub1"
            }
        }

        response = self.client.post('/post-measurements/', data1, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Measurement.objects.count(), 1)
        self.assertEqual(Alarm.objects.count(), 1)

        self.force_authenticate('hub2')

        data2 = {
            "Measurements": [
                {
                    "date": measurement_time + 50,
                    "type": "heart_rate",
                    "unit": "bpm",
                    "value": 45
                }
            ],
            "Observation": {
                "hub_id": "hub2"
            }
        }

        response = self.client.post('/post-measurements/', data2, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Measurement.objects.count(), 2)
        self.assertEqual(Alarm.objects.count(), 2)  # another alarm has been created

    def test_update_daily_activity_measurement(self):
        hub_user = self.create_hub('hub1')
        larsoverhaug = Patient.objects.get(user__username='larsoverhaug')
        larsoverhaug.hub = hub_user
        larsoverhaug.save()
        self.force_authenticate('hub1')

        measurement_time = int(time.time())
        data = {
            "Measurements": [
                {
                    "date": measurement_time,
                    "type": "steps",
                    "unit": "steps",
                    "value": 656
                }
            ],
            "Observation": {
                "hub_id": "hub1"
            }
        }

        response = self.client.post('/post-measurements/', data, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Measurement.objects.count(), 1)

        data['Measurements'][0]['value'] = 890

        response = self.client.post('/post-measurements/', data, 'json')

        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(Measurement.objects.count(), 1)
        self.assertEqual(Measurement.objects.first().value, 890)
