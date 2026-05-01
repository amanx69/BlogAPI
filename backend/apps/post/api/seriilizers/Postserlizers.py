from rest_framework import serializers
from ...models import Post ,Category
class PostCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(


        min_length=10,
        max_length=200,
        error_messages={
            'blank': 'Title cannot be empty.',
            'min_length': 'Title must be at least 10 characters.',
            'max_length': 'Title cannot exceed 200 characters.',
        }
    )
    
    slug = serializers.SlugField(
        required=False,
        error_messages={
            'invalid': 'Slug must contain only letters, numbers, and hyphens.',
        }
    )
    
    content = serializers.CharField(
        min_length=50,
        error_messages={
            'blank': 'Content cannot be empty.',
            'min_length': 'Content must be at least 50 characters.',
        }
    )
    
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
        error_messages={
            'does_not_exist': 'Selected category does not exist.',
            'incorrect_type': 'Category must be a valid ID.',
        }
    )
    
    image = serializers.ImageField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid_image': 'Please upload a valid image file.',
        }
    )
    
    status = serializers.ChoiceField(
        choices=['draft', 'published'],
        default='draft'
    )
    
    class Meta:
        model = Post
        fields = ["id",'title', 'slug', 'content', 'category', 'image', 'status']

    def validate_slug(self, value):
        if value:
            import re
            if not re.match(r'^[a-zA-Z0-9\-]+$', value):
                raise serializers.ValidationError(
                    'Slug can only contain letters, numbers, and hyphens.'
                )
            
            # Check if slug is unique (excluding current post for updates)
            if Post.objects.filter(slug=value).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise serializers.ValidationError(
                    'This slug is already taken. Please choose another.'
                )
        return value
    
   
    def validate_title(self, value):
   
        blocked_words = ['spam', 'scam', 'fake']
        
        for word in blocked_words:
            if word.lower() in value.lower():
                raise serializers.ValidationError(
                    f'Title cannot contain the word "{word}".'
                )
    
        words = value.split()
        if len(words) < 3:
            raise serializers.ValidationError(
                'Title must contain at least 3 words.'
            )
        
        return value
    def validate_content(self, value):
  
        if len(value) < 30:
            raise serializers.ValidationError(
                'Content must be at least 50 characters.'
            )
 
   
        
        return value
    
  
    def validate_image(self, value):
        if value:
            #! Check file size (max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if value.size > max_size:
                raise serializers.ValidationError(
                    'Image size cannot exceed 5MB.'
                )
            
            #! Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    f'Only JPEG, PNG, GIF, and WEBP images are allowed.'
                )
        
        return value
    def validate(self, attrs):
        status = attrs.get('status', 'draft')
        user = self.context['request'].user
        
        if status == 'published':
            # Check if user has complete profile
            if not hasattr(user, 'is_verified') or not user.is_verified:
             
                 raise serializers.ValidationError({
                     'status': 'You must verify your email before publishing.'
                 })
           
        
        if not attrs.get('slug'):
            from django.utils.text import slugify
            title = attrs.get('title', '')
            base_slug = slugify(title)
            
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            attrs['slug'] = slug
        
        return attrs
