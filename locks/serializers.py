# serializers.py
from rest_framework import serializers
from .models import LockCommand

class LockCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = LockCommand
        fields = '__all__'
