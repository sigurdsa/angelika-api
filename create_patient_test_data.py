# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User, Group
from patient.models import Patient
import random
import os
import django
from patient.helpers import generate_username
import codecs
from django.utils import timezone
from datetime import timedelta
from measurement.models import Measurement
from threshold_value.models import ThresholdValue

"""
Running this file will create 500 random patients with 500 measurements and 30 threshold values for each patient
To run this file:
$ make shell
>>> execfile('create_patient_test_data.py')
"""

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()


class CreatePatientTestData():
    def get_list_from_file(self, filename):
        dirname = os.path.dirname('__file__')
        path = os.path.join(dirname, filename)
        f = codecs.open(path, 'r', "utf-8")
        lines = [line.rstrip() for line in f]
        f.close()
        return lines

    def __init__(self):
        self.first_names_men = self.get_list_from_file('testdata_first_names_men.txt')
        self.first_names_women = self.get_list_from_file('testdata_first_names_women.txt')
        self.last_names = self.get_list_from_file('testdata_last_names.txt')

    def get_random_name(self):
        gender = random.randint(0, 1)
        num_first_names = random.randint(1, 2)
        first_names_array = self.first_names_men if gender else self.first_names_women
        first_name = ""

        for i in range(num_first_names):
            first_name += random.choice(first_names_array)
            if i != num_first_names - 1:
                first_name += " "
        last_name = random.choice(self.last_names)
        return first_name, last_name

    def get_random_birth_day(self):
        day = random.randint(1, 28)
        day = str(day)
        if len(day) < 2:
            day = '0' + day
        return day

    def get_random_birth_month(self):
        month = random.randint(1, 12)
        month = str(month)
        if len(month) < 2:
            month = '0' + month
        return month

    def get_random_birth_year(self):
        return str(random.randint(17, 55))

    def get_random_national_identification_number(self, birth_day, birth_month, birth_year):
        return birth_day + birth_month + birth_year + str(random.randint(10000, 99999))

    def get_random_phone_number(self):
        return str(random.randint(40000000, 99999999))

    def create_random_patient_with_measurements(self):
        first_name, last_name = self.get_random_name()
        birth_day = self.get_random_birth_day()
        birth_month = self.get_random_birth_month()
        birth_year = self.get_random_birth_year()
        national_identification_number = self.get_random_national_identification_number(birth_day, birth_month, birth_year)
        username = generate_username(first_name, last_name, birth_year)
        phone_number = self.get_random_phone_number()

        patient = self.create_patient(username, first_name, last_name, national_identification_number, phone_number)
        print "Created patient", patient
        self.create_random_measurements(patient)
        self.create_random_threshold_values(patient)

    def create_random_measurements(self, patient):
        num_days = 100
        then = timezone.now() - timedelta(days=num_days)
        measurements = []
        for measurement_type in ['A', 'C', 'O', 'P', 'T']:
            for i in range(num_days):
                measurement_time = then + timedelta(days=i)
                measurement_value = round(random.uniform(40, 100), 1)
                measurement = Measurement(
                    patient=patient,
                    value=measurement_value,
                    time=measurement_time,
                    type=measurement_type
                )
                measurements.append(measurement)
        Measurement.objects.bulk_create(measurements)

    def create_random_threshold_values(self, patient):
        num_days = 100
        then = timezone.now() - timedelta(days=num_days)
        threshold_values = []
        for measurement_type in ['O', 'P', 'T']:
            for i in range(int(num_days / 10) - 1):
                threshold_value_time = then + timedelta(days=i*10)
                lower_threshold_value = round(random.uniform(10, 39), 1)
                lower_threshold_value = ThresholdValue(
                    patient=patient,
                    value=lower_threshold_value,
                    time=threshold_value_time,
                    type=measurement_type,
                    is_upper_threshold=False
                )
                upper_threshold_value = round(random.uniform(100, 140), 1)
                upper_threshold_value = ThresholdValue(
                    patient=patient,
                    value=upper_threshold_value,
                    time=threshold_value_time,
                    type=measurement_type,
                    is_upper_threshold=True
                )
                threshold_values.append(lower_threshold_value)
                threshold_values.append(upper_threshold_value)
        ThresholdValue.objects.bulk_create(threshold_values)

    def create_patient(self, username, first_name, last_name, national_identification_number, phone_number):
        patient_user = User.objects.create_user(username, username + '@hotmail.com', 'test')
        patient_user.first_name = first_name
        patient_user.last_name = last_name
        patient_user.save()
        patient_user.groups.add(Group.objects.get(name='patients'))
        patient = Patient.objects.create(
            user=patient_user,
            national_identification_number=national_identification_number,
            phone_number=phone_number,
            address='arbeiderveien',
            zip_code='0030',
            city='Oslo',
            activity_access=True,
            pulse_access=False,
            o2_access=False,
            temperature_access=False
        )
        return patient


def run():
    c = CreatePatientTestData()
    num_new_users = 500
    print 'Creating 500 patients, 15 000 threshold values and 250 000 measurements. Watch your database grow.'
    for i in range(num_new_users):
        c.create_random_patient_with_measurements()
        if i > 0 and i % 50 == 0:
            print str(float(100 * i) / num_new_users) + "% done"
    print "Done!"

run()
