import json
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Triage(models.Model):
    RED = 0
    YELLOW = 1
    GREEN = 2
    BLUE = 3
    TRIAGE_RISK_CATEGORIES = [
        (RED, _('red')),
        (YELLOW, _('yellow')),
        (GREEN, _('green')),
        (BLUE, _('blue')),
    ]
    name = models.CharField(max_length=500, null=True, blank=True)
    main_complaint = models.CharField(max_length=500, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    body_temperature = models.FloatField(null=True, blank=True)
    body_mass = models.FloatField(null=True, blank=True)
    blood_glucose = models.IntegerField(null=True, blank=True)
    blood_pressure = models.CharField(max_length=200, null=True, blank=True)
    blood_oxygen_level = models.FloatField(null=True, blank=True)
    alergies = models.CharField(max_length=500, null=True, blank=True)
    continuos_medication = models.CharField(max_length=500, null=True,
                                            blank=True)
    previous_diagnosis = models.CharField(max_length=500,
                                          null=True,
                                          blank=True)
    height = models.FloatField(null=True, blank=True)
    risk_level = models.IntegerField(
            choices=TRIAGE_RISK_CATEGORIES,
            default=RED,
    )
    bot_next_type = models.CharField(max_length=50, null=True, blank=True)
    bot_next_content = models.CharField(max_length=500, null=True, blank=True)
    next_question = models.CharField(max_length=500, null=True, blank=True)

    def set_blood_pressure(self, x):
        self.blood_pressure = json.dumps(x)

    def get_blood_pressure(self):
        return json.loads(self.blood_pressure)

    def set_alergies(self, x):
        self.alergies = json.dumps(x)

    def get_alergies(self):
        return json.loads(self.alergies)

    def set_continuos_medication(self, x):
        self.continuos_medication = json.dumps(x)

    def get_continuos_medication(self):
        return json.loads(self.continuos_medication)

    def set_previous_diagnosis(self, x):
        self.previous_diagnosis = json.dumps(x)

    def get_previous_diagnosis(self):
        return json.loads(self.previous_diagnosis)
