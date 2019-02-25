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


class PlaceMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaceMap
        fields = ('id', 'user', 'places', 'continent_count', 'place_count',
                  'place_percent', 'region_count', 'un_country_count',
                  'un_country_area_percent')
        read_only_fields = ('id', 'continent_count', 'place_count',
                            'place_percent', 'region_count',
                            'un_country_count', 'un_country_area_percent')


    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user
    #     places = validated_data['places']

    #     placemap = PlaceMap.objects.create(user=user)
    #     placemap.places.add()

    #     return 
    #         user=user,
    #         )

    #     if user != request.user:
    #         raise serializers.ValidationError({
    #             'user': 'User can only create placemap for self.'
    #         })


    # def validate(self, data):
    #     user = data.get('user')

    #     if user:
    #         request = self.context.get('request')

    #         if user != request.user:
    #             raise serializers.ValidationError({
    #                 'user': 'User can only create placemap for self.'
    #             })

    #     return super().validate(data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'placemap')
        read_only_fields = ('id', 'placemap')

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
