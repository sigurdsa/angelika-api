from test.testcase import AngelikaAPITestCase
from django.contrib.auth.models import User, Group
from patient.models import Patient
from measurement.models import Measurement


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

        self.assertEqual(Measurement.objects.all().count(), 0)  # Nothing is created yet

        response = self.client.post('/post-measurements/', data, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(response.data["num_measurements"], 1)  # One object created
        self.assertEqual(Measurement.objects.all().count(), 1)  # One object created
        self.assertAlmostEqual(Measurement.objects.first().value, 1067.0)  # Correct no of steps
        self.assertEqual(Measurement.objects.first().patient, larsoverhaug)  # Correct patient

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

