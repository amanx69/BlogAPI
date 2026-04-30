from rest_framework import serializers
from ...models import Comment


class CommentSerlizer(serializers.ModelSerializer):
    
    class Meta:
        model= Comment
        fields= ["text"]
    
    


