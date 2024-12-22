from rest_framework import serializers
from django.contrib.auth.models import User

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, parsed_data):
        user_model = User(
            username=parsed_data['username'],
        )
        user_model.set_password(parsed_data['password'])
        user_model.save()
        return user_model