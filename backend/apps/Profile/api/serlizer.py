from rest_framework import serializers
from ..models import Profile





class UpdateProfileSerlizer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields= ["username","profile_pic","bio","gender","date_of_birth","phone","country","city","address","github","twitter","linkedin","instagram"]
        read_only_fields= ["id","user"]
        
        
    def validate_username(self, value):
        
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        elif len(value) > 10:
            raise serializers.ValidationError("Username must be at most 20 characters long.")
       

        return value
    def validate_bio(self, value):
        if len(value) > 60:
            raise serializers.ValidationError("Bio must be at most 60 characters long.")
        return value



class ProfileSerlizer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields= ["username","profile_pic","bio","gender","date_of_birth","phone","country","city","address","github","twitter","linkedin","instagram"]
    


class TragetProfileSerlizer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields= ["username","profile_pic","bio","gender","date_of_birth","country","city"]
        read_only_fields= ["username","profile_pic","bio","gender","date_of_birth","phone","country","city"]