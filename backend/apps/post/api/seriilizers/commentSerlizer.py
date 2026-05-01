from rest_framework import serializers
from ...models import Comment
from .Postserlizers import PostCreateSerializer

class CommentSerlizer(serializers.ModelSerializer):
    post=  PostCreateSerializer(read_only= True)
    class Meta:
        model= Comment
        fields= ["text","post","created_at"]
        
        
        
    def validate_text(self, value):
        bad_words = ['asshole', 'pussy', 'fuck']  
        if any(bad_word in value.lower() for bad_word in bad_words):
            raise serializers.ValidationError("Comment contains inappropriate language.")
        elif len(value) < 2:
            raise serializers.ValidationError("Comment must be at least 2 characters long.")
        
        return value
    
    


