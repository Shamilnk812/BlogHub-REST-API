from rest_framework import serializers
from .models import Post
from .validators import *



class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for creating, updating, and retrieving blog posts.
    Includes custom validation for title and content fields.
    """

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'excerpt', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        user = self.context['request'].user
        instance = self.instance  # it will None for create, object for update
        # validate blog title
        return validate_blog_title(value, user, instance)


    def validate_content(self, value):
        
        # Validates content 
        return validate_blog_content(value)