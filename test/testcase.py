from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from patient.models import Patient


class AngelikaAPITestCase(APITestCase):

    def setUp(self):
        Group.objects.create(name='patients')

        health_professional_group = Group.objects.create(name='health-professionals')
        health_professional_user = User.objects.create_user('helselise', 'lise@angelika.no', 'test')
        health_professional_user.save()
        health_professional_user.groups.add(health_professional_group)

        self.create_patient('larsoverhaug', 'Lars', 'Overhaug')

    def create_patient(self, username, first_name, last_name):
        patient_user = User.objects.create_user(username, username + '@hotmail.com', 'test')
        patient_user.first_name = first_name
        patient_user.last_name = last_name
        patient_user.save()
        patient_user.groups.add(Group.objects.get(name='patients'))
        patient = Patient.objects.create(
            user=patient_user,
            national_identification_number='02094523456',
            phone_number='45763984',
            address='arbeiderveien',
            zip_code='0030',
            city='Oslo',
            activity_access=True,
            pulse_access=False,
            o2_access=False,
            temperature_access=False
        )

        return patient

    def force_authenticate(self, username):
        user = User.objects.get(username=username)
        self.client.force_authenticate(user=user)
        return user
