from test.testcase import AngelikaAPITestCase
from patient.models import Patient
from next_of_kin.models import NextOfKin
from motivation_text.models import MotivationText
from measurement.models import Measurement
from alarm.models import Alarm


class PermissionTests(AngelikaAPITestCase):
    def test_patient_list_unauthorized(self):
        response = self.client.get('/patients/')
        self.assertEqual(response.status_code, 401)  # UNAUTHORIZED

    def test_patient_list(self):
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
        first_patient = Patient.objects.all().first()
        self.assertTrue(first_patient.activity_access)

        response = self.client.patch('/patients/' + str(first_patient.id) + '/', {
            'activity_access': False
        })
        self.assertFalse(response.data['activity_access'])

        first_patient = Patient.objects.all().first()
        self.assertFalse(first_patient.activity_access)

    def test_add_next_of_kin(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.all().first()

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
        first_patient = Patient.objects.all().first()

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
        first_patient = Patient.objects.all().first()

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
        first_patient = Patient.objects.all().first()

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
        first_patient = Patient.objects.all().first()

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
        first_patient = Patient.objects.all().first()

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

    def test_update_motivation_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.all().first()

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

    def test_remove_motivation_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.all().first()

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
        first_patient = Patient.objects.all().first()

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
        first_patient = Patient.objects.all().first()

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
        first_patient = Patient.objects.all().first()

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
        first_patient = Patient.objects.all().first()

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


class GetTests(AngelikaAPITestCase):
    def test_graph_data(self):
        self.force_authenticate('helselise')
        response = self.client.get('/patients/1/graph_data/?type=O')
        self.assertEqual(response.status_code, 200)  # OK
        self.assertEqual(response.data, [])


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
