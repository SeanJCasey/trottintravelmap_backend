from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, \
    MinimumLengthValidator

from rest_framework import serializers

from places.models import Country, Place, PlaceMap

User = get_user_model()


class PlaceCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ('name', 'code', 'continent')


class PlaceSerializer(serializers.ModelSerializer):
    country = PlaceCountrySerializer()

    class Meta:
        model = Place
        fields = '__all__'


class PlaceMapUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name',)


class PlaceMapSerializer(serializers.ModelSerializer):
    user = PlaceMapUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PlaceMap
        fields = ('user', 'user_id', 'places')
        read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password', 'placemap', 'slug')
        read_only_fields = ('id', 'placemap', 'slug')

    def validate(self, data):
        password = data.get('password')
        if password:
            validate_password(
                password,
                password_validators=[MinimumLengthValidator()]
            )

        return super().validate(data)

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data['email'],
            validated_data['name'],
            validated_data['password']
        )
