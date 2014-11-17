# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User, Group
from patient.models import Patient
import random
import os
import django
import codecs
from django.utils import timezone
from datetime import timedelta
from measurement.models import Measurement
from threshold_value.models import ThresholdValue
from alarm.models import Alarm

"""
Running this file will create a measurements with a alarm for up to 5000 of the patients in the system.
Up to 10 of the alarms will be untreated.
To run this file:
$ make shell
>>> execfile('create_alarm_test_data.py')
"""

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()


class CreateAlarmTestData():
    def __init__(self):
        self.num_alarms_created = 0

    def create_random_measurement(self, patient):
        measurement_time = timezone.now()
        measurement_type = random.choice(['O', 'P', 'T'])
        measurement_value = round(random.uniform(1, 30), 1)
        if random.randint(0, 1) and measurement_type != 'O':
            measurement_value += 110
        measurement = Measurement.objects.create(
            patient=patient,
            value=measurement_value,
            time=measurement_time,
            type=measurement_type
        )
        return measurement

    def create_alarm(self, measurement):
        alarm = Alarm.objects.create(
            measurement=measurement,
            is_treated=(self.num_alarms_created > 10),
            reason=(measurement.value > 50)
        )
        self.num_alarms_created += 1

        return alarm


def run():
    c = CreateAlarmTestData()
    print 'Creating alarms and measurements. Watch your database grow.'
    patients = list(Patient.objects.all()[:5000])
    num_patients = len(patients)
    random.shuffle(patients)
    i = 0
    for patient in patients:
        measurement = c.create_random_measurement(patient)
        c.create_alarm(measurement)
        i += 1
        if i % 50 == 0:
            print str(float(100 * i) / num_patients) + "% done"

    print "Done!"

run()
