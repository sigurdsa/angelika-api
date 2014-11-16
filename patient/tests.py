# -*- coding: UTF-8 -*-
from test.testcase import AngelikaAPITestCase
from patient.models import Patient
from next_of_kin.models import NextOfKin
from motivation_text.models import MotivationText
from measurement.models import Measurement
from alarm.models import Alarm
from django.utils import timezone
from datetime import timedelta
from threshold_value.models import ThresholdValue
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .helpers import generate_username


class PermissionTests(AngelikaAPITestCase):
    def test_patient_list_unauthorized(self):
        response = self.client.get('/patients/')
        self.assertEqual(response.status_code, 401)  # UNAUTHORIZED

    def test_patient_list_authorized(self):
        self.force_authenticate('helselise')
        response = self.client.get('/patients/')
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response.data['count'], 1)
        self.assertTrue('results' in response.data)

    def test_patient_list_no_permission(self):
        self.force_authenticate('larsoverhaug')
        response = self.client.get('/patients/')
        self.assertEqual(response.status_code, 403)  # PERMISSION DENIED


class PatchTests(AngelikaAPITestCase):
    def test_update_activity_access(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()
        self.assertTrue(first_patient.activity_access)

        response = self.client.patch('/patients/' + str(first_patient.id) + '/', {
            'activity_access': False
        })
        self.assertFalse(response.data['activity_access'])

        first_patient = Patient.objects.first()
        self.assertFalse(first_patient.activity_access)

    def test_add_next_of_kin(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'next_of_kin': [
                    {
                        'id': None,
                        'full_name': 'Marta Halse',
                        'address': 'Jessheims veg 32',
                        'phone_number': '46789583',
                        'relation': 'Datter'
                    }
                ]
            },
            format='json'
        )

        next_of_kin = NextOfKin.objects.filter(patient=first_patient)
        self.assertEqual(len(next_of_kin), 1)
        next_of_kin = next_of_kin.first()
        self.assertEqual(next_of_kin.full_name, 'Marta Halse')

    def test_update_next_of_kin_address(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        next_of_kin = NextOfKin.objects.create(
            patient=first_patient,
            full_name='Marit Ulstein',
            address='Gjengeskvulpet 4',
            phone_number='34780943',
            priority=0,
            relation='Datter'
        )

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'next_of_kin': [
                    {
                        'id': next_of_kin.id,
                        'full_name': 'Marit Ulstein',
                        'address': 'Jessheims veg 32',
                        'phone_number': '34780943',
                        'relation': 'Datter'
                    }
                ]
            },
            format='json'
        )

        next_of_kin = NextOfKin.objects.filter(patient=first_patient)
        self.assertEqual(len(next_of_kin), 1)
        next_of_kin = next_of_kin.first()
        self.assertEqual(next_of_kin.address, 'Jessheims veg 32')

    def test_reorder_next_of_kin(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        next_of_kin1 = NextOfKin.objects.create(
            patient=first_patient,
            full_name='Marit Ulstein',
            address='Gjengeskvulpet 4',
            phone_number='34780943',
            priority=0,
            relation='Datter'
        )

        next_of_kin2 = NextOfKin.objects.create(
            patient=first_patient,
            full_name='Marte Ulstein',
            address='Gjengeskvulpet 4',
            phone_number='45879434',
            priority=1,
            relation='Datter'
        )

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'next_of_kin': [
                    {
                        'id': next_of_kin2.id,
                        'full_name': 'Marte Ulstein',
                        'address': 'Gjengeskvulpet 4',
                        'phone_number': '45879434',
                        'relation': 'Datter'
                    },
                    {
                        'id': next_of_kin1.id,
                        'full_name': 'Marit Ulstein',
                        'address': 'Gjengeskvulpet 4',
                        'phone_number': '34780943',
                        'relation': 'Datter'
                    }
                ]
            },
            format='json'
        )

        # total count of next of kin for this patient
        next_of_kin = NextOfKin.objects.filter(patient=first_patient)
        self.assertEqual(len(next_of_kin), 2)

        # updated first next of kin
        next_of_kin1 = next_of_kin.first()
        self.assertEqual(next_of_kin1.full_name, 'Marte Ulstein')

        # updated second next of kin
        next_of_kin2 = next_of_kin.last()
        self.assertEqual(next_of_kin2.full_name, 'Marit Ulstein')

    def test_remove_next_of_kin_address(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        NextOfKin.objects.create(
            patient=first_patient,
            full_name='Marit Ulstein',
            address='Gjengeskvulpet 4',
            phone_number='34780943',
            priority=0,
            relation='Datter'
        )

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'next_of_kin': []
            },
            format='json'
        )

        next_of_kin = NextOfKin.objects.filter(patient=first_patient)
        self.assertEqual(len(next_of_kin), 0)

    def test_update_and_reorder_and_remove_and_add_next_of_kin(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        next_of_kin1 = NextOfKin.objects.create(
            patient=first_patient,
            full_name='Marit Ulstein',
            address='Gjengeskvulpet 4',
            phone_number='34780943',
            priority=0,
            relation='Datter'
        )

        next_of_kin2 = NextOfKin.objects.create(
            patient=first_patient,
            full_name='Marte Ulstein',
            address='Gjengeskvulpet 4',
            phone_number='45879434',
            priority=1,
            relation='Datter'
        )

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'next_of_kin': [
                    {
                        'id': None,
                        'full_name': 'Hans Ulstein',
                        'address': 'Jessheims veg 36',
                        'phone_number': '45987543',
                        'relation': 'Bror'
                    },
                    {
                        'id': next_of_kin1.id,
                        'full_name': 'Marit Ulstein',
                        'address': 'Jessheims veg 32',
                        'phone_number': '34780943',
                        'relation': 'Datter'
                    },
                ]
            },
            format='json'
        )

        # total count of next of kin for this patient
        next_of_kin = NextOfKin.objects.filter(patient=first_patient)
        self.assertEqual(len(next_of_kin), 2)

        next_of_kin1 = next_of_kin.first()
        self.assertEqual(next_of_kin1.address, 'Jessheims veg 36')

        # next_of_kin 2 is removed
        next_of_kin2_count = NextOfKin.objects.filter(id=next_of_kin2.id).count()
        self.assertEqual(next_of_kin2_count, 0)

        next_of_kin3 = next_of_kin.last()
        self.assertEqual(next_of_kin3.phone_number, '34780943')

    def test_add_motivation_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'motivation_texts': [
                    {
                        'id': None,
                        'text': 'HEI'
                    }
                ]
            },
            format='json'
        )

        motivation_text = MotivationText.objects.filter(type='M', patient=first_patient)
        self.assertEqual(len(motivation_text), 1)
        motivation_text = motivation_text.first()
        self.assertEqual(motivation_text.text, 'HEI')

    def test_add_motivation_text_with_sound(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'motivation_texts': [
                    {
                        'id': None,
                        'text': 'HEI',
                        'sound': {
                            'base64': "//sUxAAAA+hrJBQRAAiXEifDDIABABfgB/+QmQn8k4GBgYGBgYAAAAAAAAAIAw8PP8AAAB36vVuJiq8Bnfa265+K9XsKop+9xJ/N6ETUHJCYfwo7ghL8YYOZck4HwQh4//sUxAMABIiFQhhigAiUEijDEDAB0jnQfa9jOtSpazWZzglxd1cvOzlmIq0dTRjCXdAW8fthDJIqNcluHk7//J/OWwWZoYIdKGcmr7BTYtpQpzmJp4Vww1UQ2KOVQB7D//sUxAOARRiDRXyRAAiOBWlwBJgZxGE4HR+CUEDDC7FOyjlZ3T3WxpZ9mmn2qgUCuAIeg7m59Gc8010oHEQGZfBETlHA6Jhk6o9wcSZe/nCmbWZ+n/zfpXuGlQ3FEmnA//sUxAKARKiFQ2AkYIiRjihijDAAE2QSJgdIJh8CtYYiwrrldpfKVj8svK65yLK5UbfNYLnKv/oH/KQoGUWiyXKN1nEFRT3fPPrwiG7lc/0sfNATgIQFyLdS2r4Q2qbp//sUxAMABPiVThg4AACQEerThnABnctP/VqrZi5dM7pbEUTpMTxOMgpSn0CfLiRhD9wFAibjuFVsttHs4NEFaoEZxIUrop9P/27vsap7d9TAEDcRAdgVOfx+Qgucanq5//sUxAKARLglYeAwwICIhez0AwwunNogABwJmTssnL4DWy+RQLMDwqcJC+NZ0iIMv0DxK3WoWba7WxEihMhJIJoFSBh60jJI9w4LlkGSoAJkKlE1d7xPGRp////IkQAB//sUxAQARBwfV6AMwAB6g+nwAwwQAPgRI3cNIG88EljAKLWOTMAXkSV6ktKa1iSSS2zQHNISOszfgBAGJBsCByomdIHrkoJKfrbfHIUSW27SYBaDnkxMLZCAI5oUOPoP//sUxAmARAwjTWAkwIB8ieowAwg4gPtHOa4wgxMqOMn78YLr7fbTUdYBQFqJoRNL10I28WhFIt/vKLLM2q3qe961EcllknAAB9NwjhQigxTtLgAZPOKc2yIDsT/3luU0//sUxA8AQ/yHTYGETcB0AupwAaQEtwou1v/25SAi4fUQv7lCogCgXBFSigveATRT7SNESBbbbbZ/IANbBMiz5ZDiJbwokEDbVFYhKAHkfcadFlPF1r21syLEgDJISaZQ//sUxBYAQ+gpZYAYQPB9BSmwBIgQkRUE8NW081QnUQc3FAHoaeCeig==",
                            'is_updated': True
                        }
                    }
                ]
            },
            format='json'
        )

        motivation_text = MotivationText.objects.filter(type='M', patient=first_patient)
        self.assertEqual(len(motivation_text), 1)
        motivation_text = motivation_text.first()
        self.assertEqual(motivation_text.sound.size, 904)
        motivation_text.sound.delete(save=False)

    def test_update_motivation_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        motivation_text = MotivationText.objects.create(
            patient=first_patient,
            text='HEI',
            time_created='2014-10-24T09:46:20Z'
        )

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'motivation_texts': [
                    {
                        'id': motivation_text.id,
                        'time_created': '2014-10-24T09:46:20Z',
                        'text': 'LOL'
                    }
                ]
            },
            format='json'
        )

        motivation_texts = MotivationText.objects.filter(type='M', patient=first_patient)
        self.assertEqual(len(motivation_texts), 1)
        motivation_text = motivation_texts.first()
        self.assertEqual(motivation_text.text, 'LOL')

        # time_created should not be updated as it is read only
        self.assertNotEqual("%s" % motivation_text.time_created, '2014-10-24 09:46:20+00:00')

    def test_update_motivation_text_with_sound(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        motivation_text = MotivationText.objects.create(
            patient=first_patient,
            text='HEI',
            time_created='2014-10-24T09:46:20Z'
        )

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'motivation_texts': [
                    {
                        'id': motivation_text.id,
                        'time_created': '2014-10-24T09:46:20Z',
                        'sound': {
                            'base64': "//sUxAAAA+hrJBQRAAiXEifDDIABABfgB/+QmQn8k4GBgYGBgYAAAAAAAAAIAw8PP8AAAB36vVuJiq8Bnfa265+K9XsKop+9xJ/N6ETUHJCYfwo7ghL8YYOZck4HwQh4//sUxAMABIiFQhhigAiUEijDEDAB0jnQfa9jOtSpazWZzglxd1cvOzlmIq0dTRjCXdAW8fthDJIqNcluHk7//J/OWwWZoYIdKGcmr7BTYtpQpzmJp4Vww1UQ2KOVQB7D//sUxAOARRiDRXyRAAiOBWlwBJgZxGE4HR+CUEDDC7FOyjlZ3T3WxpZ9mmn2qgUCuAIeg7m59Gc8010oHEQGZfBETlHA6Jhk6o9wcSZe/nCmbWZ+n/zfpXuGlQ3FEmnA//sUxAKARKiFQ2AkYIiRjihijDAAE2QSJgdIJh8CtYYiwrrldpfKVj8svK65yLK5UbfNYLnKv/oH/KQoGUWiyXKN1nEFRT3fPPrwiG7lc/0sfNATgIQFyLdS2r4Q2qbp//sUxAMABPiVThg4AACQEerThnABnctP/VqrZi5dM7pbEUTpMTxOMgpSn0CfLiRhD9wFAibjuFVsttHs4NEFaoEZxIUrop9P/27vsap7d9TAEDcRAdgVOfx+Qgucanq5//sUxAKARLglYeAwwICIhez0AwwunNogABwJmTssnL4DWy+RQLMDwqcJC+NZ0iIMv0DxK3WoWba7WxEihMhJIJoFSBh60jJI9w4LlkGSoAJkKlE1d7xPGRp////IkQAB//sUxAQARBwfV6AMwAB6g+nwAwwQAPgRI3cNIG88EljAKLWOTMAXkSV6ktKa1iSSS2zQHNISOszfgBAGJBsCByomdIHrkoJKfrbfHIUSW27SYBaDnkxMLZCAI5oUOPoP//sUxAmARAwjTWAkwIB8ieowAwg4gPtHOa4wgxMqOMn78YLr7fbTUdYBQFqJoRNL10I28WhFIt/vKLLM2q3qe961EcllknAAB9NwjhQigxTtLgAZPOKc2yIDsT/3luU0//sUxA8AQ/yHTYGETcB0AupwAaQEtwou1v/25SAi4fUQv7lCogCgXBFSigveATRT7SNESBbbbbZ/IANbBMiz5ZDiJbwokEDbVFYhKAHkfcadFlPF1r21syLEgDJISaZQ//sUxBYAQ+gpZYAYQPB9BSmwBIgQkRUE8NW081QnUQc3FAHoaeCeig==",
                            'is_updated': True
                        }
                    }
                ]
            },
            format='json'
        )

        motivation_texts = MotivationText.objects.filter(type='M', patient=first_patient)
        self.assertEqual(len(motivation_texts), 1)
        motivation_text = motivation_texts.first()
        self.assertEqual(motivation_text.text, 'HEI')
        self.assertEqual(motivation_text.sound.size, 904)
        motivation_text.sound.delete(save=False)

    def test_remove_motivation_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        MotivationText.objects.create(
            patient=first_patient,
            text='HEI',
            time_created='2014-10-24T09:46:20Z',
            type='M'
        )

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'motivation_texts': []
            },
            format='json'
        )

        self.assertEqual(MotivationText.objects.filter(type='M', patient=first_patient).count(), 0)

    def test_add_information_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'information_texts': [
                    {
                        'id': None,
                        'text': 'HEI'
                    }
                ]
            },
            format='json'
        )

        information_text = MotivationText.objects.filter(type='I', patient=first_patient)
        self.assertEqual(len(information_text), 1)
        information_text = information_text.first()
        self.assertEqual(information_text.text, 'HEI')

    def test_update_information_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        information_text = MotivationText.objects.create(
            patient=first_patient,
            text='HEI',
            time_created='2014-10-24T09:46:20Z',
            type='I'
        )

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'information_texts': [
                    {
                        'id': information_text.id,
                        'time_created': '2014-10-24T09:46:20Z',
                        'text': 'LOL'
                    }
                ]
            },
            format='json'
        )

        information_texts = MotivationText.objects.filter(type='I', patient=first_patient)
        self.assertEqual(len(information_texts), 1)
        information_text = information_texts.first()
        self.assertEqual(information_text.text, 'LOL')

        # time_created should not be updated as it is read only
        self.assertNotEqual("%s" % information_text.time_created, '2014-10-24 09:46:20+00:00')

    def test_remove_information_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        MotivationText.objects.create(
            patient=first_patient,
            text='HEI',
            time_created='2014-10-24T09:46:20Z',
            type='I'
        )

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'information_texts': []
            },
            format='json'
        )

        self.assertEqual(MotivationText.objects.filter(type='I', patient=first_patient).count(), 0)

    def test_add_information_and_motivation_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.first()

        self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'information_texts': [
                    {
                        'id': None,
                        'text': 'HEI'
                    }
                ],
                'motivation_texts': [
                    {
                        'id': None,
                        'text': 'HEI'
                    }
                ]
            },
            format='json'
        )

        information_text = MotivationText.objects.filter(type='I', patient=first_patient)
        self.assertEqual(len(information_text), 1)
        information_text = information_text.first()
        self.assertEqual(information_text.text, 'HEI')
        motivation_text = MotivationText.objects.filter(type='M', patient=first_patient)
        self.assertEqual(len(motivation_text), 1)
        motivation_text = motivation_text.first()
        self.assertEqual(motivation_text.text, 'HEI')


class GetGraphDataTests(AngelikaAPITestCase):
    def test_patient_graph_data_endpoint(self):
        self.force_authenticate('helselise')
        response = self.client.get('/patients/1/graph_data/?type=O')
        self.assertEqual(response.status_code, 200)  # OK
        self.assertTrue('measurements' in response.data)
        self.assertTrue('lower_threshold_values' in response.data)
        self.assertTrue('upper_threshold_values' in response.data)

    def test_current_patient_graph_data_endpoint(self):
        user = self.force_authenticate('larsoverhaug')

        Measurement.objects.create(
            patient=user.patient,
            type='O',
            time=timezone.now() - timedelta(days=8),  # Too old to be included in the view
            value=58.0
        )
        Measurement.objects.create(
            patient=user.patient,
            type='A',
            time=timezone.now(),
            value=58.0
        )

        response = self.client.get('/current-patient/graph_data/?type=A')
        self.assertEqual(response.status_code, 200)  # OK
        self.assertTrue('measurements' in response.data)
        self.assertTrue('lower_threshold_values' in response.data)
        self.assertTrue('upper_threshold_values' in response.data)
        self.assertEqual(len(response.data['measurements']), 1)
        self.assertFalse('alarm' in response.data['measurements'][0])

    def test_current_patient_graph_data_no_permission(self):
        """
        Patient larsoverhaug does not have permission to see his own O2 data
        """
        self.force_authenticate('larsoverhaug')
        response = self.client.get('/current-patient/graph_data/?type=O')
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_graph_data_threshold_values(self):
        self.force_authenticate('helselise')
        self.create_patient('ystenes', 'Hallgeir', 'Ystenes', '02094623456')
        patient1 = Patient.objects.first()
        patient2 = Patient.objects.last()

        ThresholdValue.objects.create(
            patient=patient1,
            type='P',
            time=timezone.now() - timedelta(days=30),
            value=58.0,
            is_upper_threshold=False
        )
        ThresholdValue.objects.create(
            patient=patient1,
            type='P',
            time=timezone.now(),
            value=55.0,
            is_upper_threshold=False
        )
        ThresholdValue.objects.create(
            patient=patient1,
            type='P',
            time=timezone.now(),
            value=150.0,
            is_upper_threshold=True
        )

        # The following two threshold values are expected to not be included in the response below
        ThresholdValue.objects.create(
            patient=patient1,
            type='O',
            time=timezone.now(),
            value=100.0,
            is_upper_threshold=False
        )
        ThresholdValue.objects.create(
            patient=patient2,
            type='P',
            time=timezone.now(),
            value=120.0,
            is_upper_threshold=True
        )

        response = self.client.get('/patients/' + str(patient1.id) + '/graph_data/?type=P')
        self.assertEqual(len(response.data['lower_threshold_values']), 2)
        self.assertEqual(len(response.data['upper_threshold_values']), 1)

        self.assertAlmostEqual(response.data['lower_threshold_values'][1]['y'], 55.0)
        self.assertAlmostEqual(response.data['upper_threshold_values'][0]['y'], 150.0)

        try:
            unix_time = int(response.data['upper_threshold_values'][0]['x'])
            self.assertGreater(unix_time, 1400000000000)  # May 13, 2014
        except ValueError:
            self.fail("x in the first object in upper_threshold_values has unexpected format."
                      " It should be an int (unix time).")

    def test_graph_data_measurements(self):
        self.force_authenticate('helselise')
        self.create_patient('ystenes', 'Hallgeir', 'Ystenes', '02094523456')
        patient1 = Patient.objects.first()
        patient2 = Patient.objects.last()

        Measurement.objects.create(
            patient=patient1,
            type='O',
            time=timezone.now() - timedelta(days=1),
            value=60.0
        )
        Measurement.objects.create(
            patient=patient1,
            type='O',
            time=timezone.now(),
            value=58.0
        )

        # The following two measurements are expected to not be included in the response below
        Measurement.objects.create(
            patient=patient1,
            type='A',
            time=timezone.now(),
            value=600
        )
        Measurement.objects.create(
            patient=patient2,
            type='O',
            time=timezone.now(),
            value=600
        )
        Measurement.objects.create(
            patient=patient1,
            type='O',
            time=timezone.now() - timedelta(days=370),  # Too old to be included in the view
            value=58.0
        )

        response = self.client.get('/patients/' + str(patient1.id) + '/graph_data/?type=O')
        self.assertEqual(len(response.data['measurements']), 2)
        self.assertAlmostEqual(response.data['measurements'][1]['y'], 58.0)

    def test_graph_data_alarms(self):
        self.force_authenticate('helselise')
        patient1 = Patient.objects.first()

        Measurement.objects.create(
            patient=patient1,
            type='O',
            time=timezone.now() - timedelta(days=1),
            value=60.0
        )
        measurement2 = Measurement.objects.create(
            patient=patient1,
            type='O',
            time=timezone.now(),
            value=58.0
        )

        alarm = Alarm.objects.create(
            measurement=measurement2,
            time_created=timezone.now()
        )

        response = self.client.get('/patients/' + str(patient1.id) + '/graph_data/?type=O')
        self.assertEqual(len(response.data['measurements']), 2)
        self.assertTrue('alarm' in response.data['measurements'][0])
        self.assertEqual(response.data['measurements'][0]['alarm'], None)
        self.assertEqual(response.data['measurements'][1]['alarm']['is_treated'], False)


class CurrentPatientTests(AngelikaAPITestCase):
    def test_call_me_request(self):
        user = self.force_authenticate('larsoverhaug')
        response = self.client.post('/current-patient/call_me/', {}, format='json')
        self.assertEqual(response.data['status'], 'ok')

        num_measurements = Measurement.objects.filter(
            patient=user.patient,
            type='C',  # CALL_ME_REQUEST
        ).count()
        num_alarms = Alarm.objects.filter(
            measurement__patient=user.patient,
            measurement__type='C',  # CALL_ME_REQUEST
        ).count()
        self.assertEqual(num_measurements, 1)
        self.assertEqual(num_alarms, 1)
        alarm = Alarm.objects.first()
        self.assertEqual(alarm.reason, None)

    def test_call_me_request_repeatedly(self):
        user = self.force_authenticate('larsoverhaug')
        response = self.client.post('/current-patient/call_me/', {}, format='json')
        self.assertEqual(response.data['status'], 'ok')
        response = self.client.post('/current-patient/call_me/', {}, format='json')
        self.assertEqual(response.data['status'], 'already_requested')

        num_requested = Measurement.objects.filter(
            patient=user.patient,
            type='C',  # CALL_ME_REQUEST
        ).count()
        self.assertEqual(num_requested, 1)

    def test_call_me_request_repeatedly_after_timeout(self):
        user = self.force_authenticate('larsoverhaug')
        response = self.client.post('/current-patient/call_me/', {}, format='json')
        self.assertEqual(response.data['status'], 'ok')

        call_me_request = Measurement.objects.get(
            patient=user.patient,
            type='C',  # CALL_ME_REQUEST
        )
        call_me_request.time = timezone.now() - timedelta(minutes=6)
        call_me_request.save()

        response = self.client.post('/current-patient/call_me/', {}, format='json')
        self.assertEqual(response.data['status'], 'ok')

        num_requested = Measurement.objects.filter(
            patient=user.patient,
            type='C',  # CALL_ME_REQUEST
        ).count()
        self.assertEqual(num_requested, 2)


class PostTests(AngelikaAPITestCase):
    def test_create_patient(self):
        self.force_authenticate('helselise')

        response = self.client.post(
            '/patients/',
            {
                'id': None,

                'user': {
                    'first_name': 'Per',
                    'last_name': 'Sprellemann'
                },

                'national_identification_number': "13057675847",
                'phone_number': '95764837',
                'address': 'Arbeiderveien 4',
                'zip_code': '0350',
                'city': 'Oslo',
                'o2_max': 100,
                'o2_min': 60,
                'pulse_max': 180,
                'pulse_min': 50,
                'temperature_max': 42,
                'temperature_min': 35,
                'activity_access': True,
                'o2_access': False,
                'pulse_access': False,
                'temperature_access': False,
                'show_activity': True,
                'show_o2': False,
                'show_pulse': True,
                'show_temperature': False,

                'next_of_kin': [
                    {
                        'full_name': 'Harald Sprellemann',
                        'address': 'Eventyrskogen',
                        'phone_number': '453548598',
                        'relation': 'Bror'
                    },
                    {
                        'full_name': 'Trond Sprellemann',
                        'address': 'Eventyrskogen',
                        'phone_number': 'har ikke tlf',
                        'relation': 'Far'
                    }
                ],
                'motivation_texts': [
                    {'text': 'Det er sol i dag! :)'}
                ],
                'information_texts': [
                    {'text': 'Info skal inn her'}
                ]
            },
            'json'
        )

        self.assertEqual(response.status_code, 201)  # Created
        self.assertTrue('user' in response.data)
        self.assertEqual(User.objects.last().last_name, "Sprellemann")
        self.assertEqual(User.objects.last().username, "pes")
        self.assertEqual(Patient.objects.last().national_identification_number, "13057675847")
        self.assertEqual(Patient.objects.last().activity_access, True)
        self.assertEqual(Patient.objects.last().show_temperature, False)
        self.assertEqual(NextOfKin.objects.count(), 2)
        self.assertEqual(NextOfKin.objects.last().full_name, 'Trond Sprellemann')
        self.assertEqual(MotivationText.objects.count(), 2)
        self.assertEqual(MotivationText.objects.filter(type='M').first().text, 'Det er sol i dag! :)')
        self.assertEqual(MotivationText.objects.filter(type='I').first().text, 'Info skal inn her')
        self.assertEqual(ThresholdValue.objects.count(), 6)

    def test_create_patient_with_minimum_amount_of_data(self):
        self.force_authenticate('helselise')

        response = self.client.post(
            '/patients/',
            {
                'user': {
                    'first_name': 'Bent',
                    'last_name': 'Hanskemann'
                },

                'national_identification_number': "05074576384",
            },
            'json'
        )

        self.assertEqual(response.status_code, 201)  # Created
        self.assertTrue('user' in response.data)
        self.assertEqual(User.objects.last().last_name, "Hanskemann")
        self.assertEqual(Patient.objects.last().national_identification_number, "05074576384")
        self.assertEqual(NextOfKin.objects.count(), 0)
        self.assertEqual(MotivationText.objects.count(), 0)
        self.assertEqual(ThresholdValue.objects.count(), 0)

    def test_unique_national_identification_number(self):
        self.force_authenticate('helselise')

        data = {
            'user': {
                'first_name': 'Bent',
                'last_name': 'Hanskemann'
            },
            'national_identification_number': "05074576384",
        }

        response = self.client.post('/patients/', data, 'json')

        self.assertEqual(response.status_code, 201)  # Created
        self.assertEqual(Patient.objects.last().national_identification_number, "05074576384")

        response2 = self.client.post('/patients/', data, 'json')
        self.assertEqual(response2.status_code, 409)  # Conflict


class UsernameHelperTests(APITestCase):
    def test_generate_username(self):
        usernames = set()
        for i in range(30):
            username = generate_username('Glenn', u'Halsten Haraldsen', '90')
            User.objects.create_user(username, username + '@angelika.no', 'test')
            self.assertFalse(username in usernames)
            usernames.add(username)

    def test_generate_username_from_weird_characters(self):
        username = generate_username(u'blablabla"#¤%¤#%=(/(', u'æåøÆØÅØ=)"#¤sfsdf', 'dfjh')
        self.assertFalse(u'ø' in username)
        self.assertFalse(u'#' in username)
