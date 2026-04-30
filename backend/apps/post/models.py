from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name




class Postmanager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted= False)
    
    

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    objects= Postmanager()
    all_objects= models.Manager()
    #! auto assing slug
    def save(self, *args, **kwargs) :
        self.slug=slugify(self.title)
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

#! like model
class Like(models.Model):
    post= models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_like")
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="like_user")
    created_at= models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user.email}like to{self.post.title}"
    
    class Meta:
    
        ordering = ['-created_at']
        unique_together = ('post', 'user') 
        

#! comment model

class Comment(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text= models.TextField(null= True,blank= True)
    created_at= models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return f"comment by{self.user.email} on {self.post.title}"
    class Mata:
        ordering = ['-created_at']
    