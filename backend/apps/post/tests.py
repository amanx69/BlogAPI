from apps.post.models import Post
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

User= get_user_model()



class PostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.user.is_verify = True
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        #!  test  create post 

    def test_create_post(self):
        data={
            "title": "Test Post dvvffnec fncdskc dcc dcnjnvdskcd dcdjcndc d",
            "content": "This is a test post vfvnfjvfdvfv vfdnvfdv fdvfd v v fdvfdvc sdc n vcfdv dncd  n n .",
            "status": "draft",
          
        }
        response = self.client.post('/api/post/post/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        #! test create post with missing fields
    def test_missing_fields(self):
        data={}
        response = self.client.post('/api/post/post/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        #! update post test
    def test_update_post(self):
        post = Post.objects.create(
            title="Original Title and there  post is created by test user",
            content="Original content  i am gay.  with sex with many peopel",
            status="draft",
            user=self.user
        )
        print(post)
        data={
            "title": "Updated Title  check this out edit compleate and there  with and tere post is created by test user",
            "status": "published"
        }
        response = self.client.patch(f'/api/post/post/{post.id}/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    #! test update post with missing fields
    def test_update_post_missing_fields(self):
        
        post = Post.objects.create(
            title="Original Title and there  post is created by test user",
            content="Original content  i",
            user=self.user
        )
        res= self.client.patch(f'/api/post/post/{post.id}/', {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
       
     


