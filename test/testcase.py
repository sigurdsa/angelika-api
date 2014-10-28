from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from patient.models import Patient


class AngelikaAPITestCase(APITestCase):

    def setUp(self):
        health_professional_group = Group.objects.create(name='health-professionals')
        patient_group = Group.objects.create(name='patients')

        health_professional_user = User.objects.create_user('helselise', 'lise@angelika.no', 'test')
        health_professional_user.save()
        health_professional_user.groups.add(health_professional_group)

        patient_user = User.objects.create_user('larsoverhaug', 'larsoverhaug@hotmail.com', 'test')
        patient_user.first_name = "Lars"
        patient_user.last_name = "Overhaug"
        patient_user.save()
        patient_user.groups.add(patient_group)
        patient = Patient.objects.create(
            hub_id='hub-trd-1',
            user=patient_user,
            national_identification_number='02094523456',
            phone_number='45763984',
            address='arbeiderveien',
            zip_code='0030',
            city='Oslo',
            pulse_max=180,
            pulse_min=49,
            o2_max=100,
            o2_min=70,
            temperature_max=41,
            temperature_min=35,
            activity_access=True,
            pulse_access=False,
            o2_access=False,
            temperature_access=False
        )

    def force_authenticate(self, username):
        user = User.objects.get(username=username)
        self.client.force_authenticate(user=user)
        return user
