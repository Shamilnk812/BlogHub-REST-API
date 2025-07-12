import re
from rest_framework import serializers
from .models import Post

def validate_blog_title(value, user, instance=None):
    """
      Validates the blog post title to ensure quality, uniqueness, and formatting.
    - Title must not be empty or just whitespace.
    - Title must not be numeric-only.
    - Title must not contain invalid patterns like '___', '...', or '._'.
    - Title must be unique per author (case-insensitive), except when updating the current instance.
    """
    
    value = value.strip()

    if not value:
        raise serializers.ValidationError("Title cannot be empty or just whitespace.")

    if value.isdigit():
        raise serializers.ValidationError("Title cannot be only numbers.")

    if re.search(r'(___|\.{3,}|_\.)', value):
        raise serializers.ValidationError("Title cannot contain sequences like '___', '...', or '._'.")

    # Skip uniqueness check if updating and title hasn't changed
    if Post.objects.filter(title__iexact=value, author=user).exclude(id=getattr(instance, 'id', None)).exists():
        raise serializers.ValidationError("You already have a post with this title.")

    return value


def validate_blog_content(value):
    """
    Validates blog content for:
    - Non-empty
    - Min and max length
    - No repeated symbols
    - No excessive links
    """
    value = value.strip()

    if not value:
        raise serializers.ValidationError("Content cannot be empty.")

    if len(value) < 10:
        raise serializers.ValidationError("Content is too short. Minimum 10 characters required.")

    if len(value) > 10000:
        raise serializers.ValidationError("Content is too long. Maximum 10,000 characters allowed.")

    if re.search(r'([!@#$%^&*(),.?":{}|<>~`=_\-\[\]])\1{5,}', value):
        raise serializers.ValidationError("Content contains spam-like repeated symbols.")

    if value.lower().count('http://') + value.lower().count('https://') > 5:
        raise serializers.ValidationError("Content contains too many links.")

    return value
