from rest_framework import serializers
from .models import Triage


class TriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triage
        fields = ('name', 'age', 'body_temperature', 'body_mass',
                  'blood_pressure', 'blood_oxygen_level', 'main_complaint',
                  'alergies', 'continuos_medication', 'previous_diagnosis',
                  'height', 'risk_level')
