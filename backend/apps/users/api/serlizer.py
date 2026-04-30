from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from ..service.get_verification_token import generate_verification_token
from ..service.email import signup_verifiction

User= get_user_model()
class SignupSerlizer(serializers.ModelSerializer):
    
    class Meta:
        model= User
        fields=["uuid","email","password"]
        
        
        
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value.lower()
 
    def validate_password(self, value):
        validate_password(value)   
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        #! send verifiction email
        uid ,token =generate_verification_token(user)
        
        print(f"{uid}/{token}")
        signup_verifiction.send_verifiction_link.delay(user.email,uid,token)
        
        return user
 

class Loginserlizer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    
    def validate(self, data):
        email= data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
        else:
            raise serializers.ValidationError("Must include email and password")

        data['user'] = user
        return data

   
        
    
        
        