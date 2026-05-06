from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class TestLoginSignup(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="simple@gmail.com",
            password="Ashu@12445d"
        )
        self.login_url  = "/api/auth/login/"
        self.signup_url = "/api/auth/signup/"
        self.logout_url = "/api/auth/Logout/"

  
    #! signup test
    def test_signup_success(self):
        data = {"email": "newuser@gmail.com", "password": "Amankumar@14"}
        res = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", res.data)
        print("done signup test")

    def test_signup_missing_fields(self):
        res = self.client.post(self.signup_url, {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        print("done signup missing fields test")

    def test_signup_duplicate_email(self):
       
        data = {"email": "simple@gmail.com", "password": "Ashu@12445d"}
        res = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        print("done signup duplicate email test")
    #! login test

    def test_login_success(self):
    
        data = {"email": "simple@gmail.com", "password": "Ashu@12445d"}
        res = self.client.post(self.login_url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        print("done login test")
        

    def test_login_missing_fields(self):
        res = self.client.post(self.login_url, {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        print("done login missing fields test")
        
        
    #!send verifiction email test
    def test_resend_verification_email(self):
        data = {"email": "simple@gmail.com"}
        res= self.client.post("/api/auth/resent-ver/", data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("message", res.data)
        print("done resend verification email test")
        
    # def test_send_nonexistent_email_verification(self):
    #     res=self.client.post("/api/auth/resent-ver/",{"email":"axxmm@gmail.com"}, format='json')
    #     print(res.status_code)
    #     self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_send_already_verified_email(self):
        self.user.is_verify = True
        self.user.save()
        res=self.client.post("/api/auth/resent-ver/",{"email":"simple@gmail.com"}, format='json')
        print(res.status_code)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        print("done send already verified email test")
        
        
        
    def gernate_verification_token(self):
        data= {"email":"simple@gmail.com"}
        res= self.client.post("/api/auth/resent-ver/", data, format='json')
        data= res.data
        return data['uid'], data['token']
        
       
    #! test email verifiction
    def test_email_verification(self):
        uid, token = self.gernate_verification_token()
        res = self.client.get(f"/api/auth/verify-email/{uid}/{token}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("message", res.data)
        print("done email verification test")
        
        
    #! def logout test
    def _get_tokens(self):
   
        res = self.client.post(self.login_url, {
            "email": "simple@gmail.com",
            "password": "Ashu@12445d"
        }, format='json')
        return res.data  
    
    
    def test_logout(self):
        tokens = self._get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        res = self.client.post(self.logout_url, {
            "refresh": tokens['refresh']
        }, format='json')

        self.assertEqual(res.status_code, status.HTTP_205_RESET_CONTENT)
        print("done logout test")
        
        
    
    