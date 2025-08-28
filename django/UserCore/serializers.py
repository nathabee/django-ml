from rest_framework import serializers
from django.contrib.auth.models import  Group
 

from rest_framework import serializers    
 
from .models import CustomUser  
 
 

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'roles', 'password','lang']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        lang = validated_data.pop('lang', None)  # Ensure that lang is correctly popped
    
        roles = validated_data.pop('roles', [])
        password = validated_data.pop('password')  # Extract the password
        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash the password
            
        if lang:
            user.lang = lang  # Set the preferred language to the user model
        

        user.save()

        # Assign the user to the specified roles (groups)
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)

        return user

    def to_representation(self, instance):
        """Modify the output to include the user's groups as roles."""
        rep = super().to_representation(instance)
        rep['roles'] = [group.name for group in instance.groups.all()]
        return rep
    
 