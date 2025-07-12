from rest_framework import generics,permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Post
from .serializers import *
from .utils import CustomPostPagination,success_response, error_response
from .permissions import IsAuthorOrReadOnly

#-------------------------- Post Creation and Listing ------------------------

class PostListCreateView(generics.ListCreateAPIView):
    """
    API view to list all blog posts or create a new post.

    - GET:
        - Public endpoint.
        - Returns a paginated list of posts (excluding soft-deleted ones).
        - Ordered by latest created.
    
    - POST:
        - Only accessible to authenticated users.
        - Allows creation of a new blog post.

    Expected JSON payload for POST:
    {
        "title": "string",        # Required, must be unique per author
        "content": "string",      # Required, minimum 10 characters
        "excerpt": "string",      # Optional, brief summary of the post
        "is_published": true      # Optional, defaults to false
    }

    Notes:
    - The `author` field is automatically assigned from the authenticated user.
    - `is_deleted=True` posts are never included in the response.
    - Pagination is applied using `CustomPostPagination`.
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPostPagination
    
    def get_queryset(self):
        return Post.objects.filter(is_deleted=False).order_by('-created_at')

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)  
            return Response(
                success_response("Your post was successfully created.", serializer.data),
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                error_response("Post creation failed due to validation error.", e.detail),
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




#--------------------------- Post update , retrive and delete ------------------------

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single blog post.

    - GET:
        - Public endpoint.
        - Returns detailed information of a single blog post by ID.

    - PUT/PATCH:
        - Only the post's author is allowed to update.
        - Supports full or partial update.
        - Automatically ignores any attempt to change the `author` field.

    - DELETE:
        - Only the post's author can delete.
        - Performs a soft delete by setting `is_deleted=True`.

    Notes:
    - Posts marked as `is_deleted=True` will not be returned.
    - Requires authentication for update and delete.
    - Uses `IsAuthorOrReadOnly` permission to enforce ownership.
    """
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    #  Returns only posts that are not soft-deleted.
    def get_queryset(self):
        return Post.objects.filter(is_deleted=False)
    
    #  Updates a blog post if the user is the author.
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                success_response("Post updated successfully.", serializer.data),
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                error_response("Update failed due to validation errors.", e.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        
    # Soft-deletes a blog post by setting `is_deleted=True`.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(
            success_response("Post deleted successfully."),
            status=status.HTTP_204_NO_CONTENT
        )
