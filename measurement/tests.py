from test.testcase import AngelikaAPITestCase
from patient.models import Patient
from measurement.models import Measurement
from threshold_value.models import ThresholdValue
from alarm.models import Alarm
import time


class PostMeasurementTests(AngelikaAPITestCase):
    def create_and_authenticate_hub(self):
        hub_user = self.create_hub('hub1')
        self.patient = Patient.objects.get(user__username='larsoverhaug')
        self.patient.hub = hub_user
        self.patient.save()
        self.force_authenticate('hub1')

    def test_post_ignored_measurements(self):
        self.create_and_authenticate_hub()

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
        self.assertEqual(Measurement.objects.first().patient, self.patient)  # Correct patient
        self.assertEqual(Alarm.objects.count(), 0)

    def test_post_when_not_authenticated(self):
        response = self.client.post('/post-measurements/', {}, 'json')
        self.assertEqual(response.status_code, 401)

    def test_post_bad_hub_id(self):
        self.create_and_authenticate_hub()
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
        self.create_and_authenticate_hub()

        ThresholdValue.objects.create(
            value=49,
            patient=self.patient,
            type='P',
            is_upper_threshold=False,
        )
        ThresholdValue.objects.create(
            value=165,
            patient=self.patient,
            type='P',
            is_upper_threshold=True,
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
        self.assertEqual(Alarm.objects.first().is_measurement_too_high, False)

    def test_post_abnormal_high_measurement(self):
        self.create_and_authenticate_hub()

        ThresholdValue.objects.create(
            value=49,
            patient=self.patient,
            type='P',
            is_upper_threshold=False,
        )
        ThresholdValue.objects.create(
            value=165,
            patient=self.patient,
            type='P',
            is_upper_threshold=True,
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
        self.assertEqual(Alarm.objects.first().is_measurement_too_high, True)

    def test_post_high_o2_measurement(self):
        self.create_and_authenticate_hub()

        ThresholdValue.objects.create(
            value=60,
            patient=self.patient,
            type='O',
            is_upper_threshold=False,
        )
        ThresholdValue.objects.create(
            value=85,
            patient=self.patient,
            type='O',
            is_upper_threshold=True,
        )

        measurement_time = int(time.time()) + 10000
        data = {
            "Measurements": [
                {
                    "date": measurement_time,
                    "type": "spo2",
                    "unit": "percent",
                    "value": 89
                }
            ],
            "Observation": {
                "hub_id": "hub1"
            }
        }

        response = self.client.post('/post-measurements/', data, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Measurement.objects.count(), 1)
        self.assertEqual(Alarm.objects.count(), 0)  # no alarm is created for a "too high" O2 value

    def test_post_abnormal_low_measurements_repeatedly(self):
        self.create_and_authenticate_hub()

        ThresholdValue.objects.create(
            value=49,
            patient=self.patient,
            type='P',
            is_upper_threshold=False,
        )
        ThresholdValue.objects.create(
            value=165,
            patient=self.patient,
            type='P',
            is_upper_threshold=True,
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
        self.create_and_authenticate_hub()

        hub_user2 = self.create_hub('hub2')
        kristin = self.create_patient('kristin', 'Kristin Hegine', 'Taraldsen', '08105534879')
        kristin.hub = hub_user2
        kristin.save()

        ThresholdValue.objects.create(
            value=49,
            patient=self.patient,
            type='P',
            is_upper_threshold=False,
        )
        ThresholdValue.objects.create(
            value=165,
            patient=self.patient,
            type='P',
            is_upper_threshold=True,
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
            is_upper_threshold=True,
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
        self.create_and_authenticate_hub()

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
