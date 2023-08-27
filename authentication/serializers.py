from rest_framework import serializers
from .models import Authentication


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50,min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = Authentication
        fields = ['username','first_name','last_name','user_type','password']