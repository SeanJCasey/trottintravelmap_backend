from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, \
    MinimumLengthValidator

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        read_only_fields = ('id',)

    def validate(self, data):
        password = data.get('password')
        validate_password(
            password,
            password_validators=[MinimumLengthValidator()]
        )

        return super().validate(data)

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data['email'], validated_data['password'])
