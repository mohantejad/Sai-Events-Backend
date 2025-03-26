import os
from django.conf import settings
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Address
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email') 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'profile_picture')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'postal_code', 'country']

class UserUpdateSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "profile_picture", "addresses"]

    def update(self, instance, validated_data):
        profile_picture = validated_data.pop("profile_picture", None)
        if profile_picture:
            old_path = os.path.join(settings.MEDIA_ROOT, str(instance.profile_picture))
            if os.path.exists(old_path):
                os.remove(old_path)
            instance.profile_picture = profile_picture
        addresses_data = validated_data.pop("addresses", [])
        instance = super().update(instance, validated_data)
        # instance.addresses.all().delete()

        for address_data in addresses_data:
            address_id = address_data.get("id")

            if address_id:
                try:
                    address_instance = Address.objects.get(id=address_id, user=instance)
                    for key, value in address_data.items():
                        setattr(address_instance, key, value)
                    address_instance.save()
                except Address.DoesNotExist:
                    continue
            else:
                Address.objects.create(user=instance, **address_data)

        instance.save()
        return instance
    

