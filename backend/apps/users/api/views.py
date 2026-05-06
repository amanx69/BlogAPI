from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import logging
from rest_framework.generics import CreateAPIView
from .serlizer import SignupSerlizer ,Loginserlizer
from ..service.gernateJwt import get_token
from  django.utils.decorators import  method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework.permissions import AllowAny
from django.contrib.auth import  get_user_model
from ..service.get_verification_token import generate_verification_token
from ..service.email import signup_verifiction
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
#! signup

User= get_user_model()
class Signup(CreateAPIView):
    serializer_class = SignupSerlizer
    permission_classes =[AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.save()
        return Response(
            {
                "message": "Account created successfully. Please verify your email.",
                "email":user.email
                       
            },
            status=status.HTTP_201_CREATED,
        )
 

#! login
class Loginview(APIView):
    permission_classes=[AllowAny]
    
    @method_decorator(ratelimit(key="ip",rate="3/m",block=True,method="POST"))
    def post(self,request):
        ser=Loginserlizer(data=request.data)
        ser.is_valid(raise_exception=True)
        user= ser.validated_data['user']
        print(user)
        token=get_token(user)
        return Response({
            "message":"Login done",
            "refresh":token['refresh'],
            "access":token['access'],
            "user":{
                "email":user.email,
                "id":user.id
            }
        },status.HTTP_200_OK)
#! verify email
class VerifyEmail(APIView):
    
    def get(self, request, uid, token):
   
        try:
            user_id = urlsafe_base64_decode(uid).decode()
        except Exception:
            return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_verify:
            return Response(
                {"error": "Email already verified"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
      
        if user.verification_token and user.verification_token != token:
            return Response(
                {"error": "This link has already been used. Please request a new one."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
     
        if not user.verification_token:
            return Response(
                {"error": "No verification token found. Please request a new one."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if default_token_generator.check_token(user, token):
            user.is_verify = True
            user.verification_token=None
            user.save()
            
            new_token = get_token(user)
            return Response({
                "message": "Email verified successfully",
                "token": new_token
            },status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
#! resend verifiction
class ResendVerificationView(APIView):
    permission_classes = []
    @method_decorator(ratelimit(key="ip",rate="3/m",block=True,method="POST"))
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error":"email are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': "email not found"},status=status.HTTP_404_NOT_FOUND)
        
        if  user.is_verify:
            return Response({'message': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)
        

        uid, token= generate_verification_token(user)
        signup_verifiction.send_verifiction_link.delay(user.email,uid,token)
        
        
        return Response({
            #TODO for testing purpose we are sending uid and token in response but in production we should not send it in response
            "uid": uid,
            "token": token,
            'message': 'Verification email sent.'}, status=status.HTTP_200_OK)




#! logot view

logger= logging.getLogger(__name__)

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return Response({"error": "somthing went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    