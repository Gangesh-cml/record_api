from rest_framework import serializers
from .models import record
from rest_framework.serializers import ValidationError

class recordSerializer(serializers.ModelSerializer):
    class Meta:
        model = record
        fields = "__all__"
