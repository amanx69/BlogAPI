from django.test import TestCase
from rest_framework.test import APIClient ,APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User= get_user_model()


class TestLoginSignup(APITestCase):
    
    def setUp(self):
        self.client= APIClient()
        self.user= User.objects.create(
            email="simple@gmail.com",
            password= "Ashu@12445d"
        )
        
        
    def test_signup_api(self):
        data = {"email": "dsimple@gmail.com", "password": "Amankumar@14"}
        res = self.client.post("/api/auth/signup/", data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("message",res.data)
        
    def test_signup_missing(self):
        
        res= self.client.post("/api/auth/signup/",{})
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
