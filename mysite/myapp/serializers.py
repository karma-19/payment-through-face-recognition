import imp
from rest_framework import serializers
from .models import UserSignupModel
class UserSignupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSignupModel
        fields = '__all__'