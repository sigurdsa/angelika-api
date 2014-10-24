from test.testcase import AngelikaAPITestCase
from patient.models import Patient
from next_of_kin.models import NextOfKin
from motivation_text.models import MotivationText


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

        response = self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'next_of_kin': [
                    {
                        'id': None,
                        'full_name': 'Marta Halse',
                        'address': 'Jessheims veg 32',
                        'phone_number': '46789583',
                        'priority': 0,
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

        response = self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'next_of_kin': [
                    {
                        'id': next_of_kin.id,
                        'full_name': 'Marit Ulstein',
                        'address': 'Jessheims veg 32',
                        'phone_number': '34780943',
                        'priority': 0,
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

    def test_remove_next_of_kin_address(self):
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

        response = self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'next_of_kin': []
            },
            format='json'
        )

        next_of_kin = NextOfKin.objects.filter(patient=first_patient)
        self.assertEqual(len(next_of_kin), 0)

    def test_update_and_remove_and_add_next_of_kin_address(self):
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

        response = self.client.patch(
            '/patients/' + str(first_patient.id) + '/',
            {
                'next_of_kin': [
                    {
                        'id': next_of_kin1.id,
                        'full_name': 'Marit Ulstein',
                        'address': 'Jessheims veg 32',
                        'phone_number': '34780943',
                        'priority': 0,
                        'relation': 'Datter'
                    },
                    {
                        'id': None,
                        'full_name': 'Hans Ulstein',
                        'address': 'Jessheims veg 36',
                        'phone_number': '45987543',
                        'priority': 1,
                        'relation': 'Bror'
                    },
                ]
            },
            format='json'
        )

        # total count of next of kin for this patient
        next_of_kin = NextOfKin.objects.filter(patient=first_patient)
        self.assertEqual(len(next_of_kin), 2)

        # first next of kin updated address
        next_of_kin1 = NextOfKin.objects.get(id=next_of_kin1.id)
        self.assertEqual(next_of_kin1.address, 'Jessheims veg 32')

        # next_of_kin 2 is removed
        next_of_kin2_count = NextOfKin.objects.filter(id=next_of_kin2.id).count()
        self.assertEqual(next_of_kin2_count, 0)

        # next of kin 3 is added
        next_of_kin3 = next_of_kin.last()
        self.assertEqual(next_of_kin3.phone_number, '45987543')

    def test_add_motivation_text(self):
        self.force_authenticate('helselise')
        first_patient = Patient.objects.all().first()
        motivation_text = MotivationText(
            patient = first_patient,
            time_created = '2014-10-24T09:46:20Z',
            text = 'HEI'
        )

        self.assertEqual(motivation_text.text, 'HEI')



