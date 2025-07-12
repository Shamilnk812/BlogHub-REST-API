from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status

from .serializers import UserRegistrationSerializer
from .models import User




# ----------------------- User Registration -----------------------


class UserRegistrationView(APIView):
    """
    Handles user registration.

    This view allows new users to register by providing a unique username, a valid email address,
    a password, and a confirm password field. It validates the input data using the 
    UserRegistrationSerializer, creates the user if the data is valid, and returns a success message
    along with the registered user's email and username. If the validation fails, it returns 
    appropriate error details. Any unexpected errors are caught and a generic error response is returned.

    Expected Input:
    - username: str (required, unique)
    - email: str (required, unique, valid email format)
    - password: str (required)
    - confirm_password: str (must match password)

    Returns:
    - 201 Created: On successful registration
    - 400 Bad Request: If validation fails
    - 500 Internal Server Error: For unexpected errors
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                response_data = {
                    'status': 'success',
                    'message': 'User registered successfully',
                    'data': {
                        'email': user.email,
                        'username': user.username,
                    },
                    
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            
            return Response({
                'status': 'failed',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'status': 'failed',
                'message': 'An unexpected error occurred during registration. Please try again later.',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        


class UserLoginView(APIView):
    """
    Handles user login.

    This view authenticates users by verifying the provided email and password. It first validates
    the input fields and email format, then checks whether a user with the given email exists.
    If authentication is successful, it returns JWT access and refresh tokens along with the user's
    email and username. If any step fails, an appropriate error message is returned.

    Expected Input:
    - email: str (required, must be in valid format)
    - password: str (required)

    Returns:
    - 200 OK: On successful authentication, along with access and refresh tokens
    - 400 Bad Request: If required fields are missing or email format is invalid
    - 401 Unauthorized: If user does not exist or credentials are invalid
    """
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        if not email or not password:
            return Response({
                'status': 'error',
                'message': 'Email and password are required.',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.filter(email__iexact=email).first()
            if user and user.check_password(password):
            
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 'success',
                    'message': 'Login successful',
                    'data': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'email': user.email,
                        'username': user.username
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'failed',
                    'message': 'Invalid email or password.'
                }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                'status': 'failed',
                'message': 'An unexpected error occurred. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UserLogoutView(APIView):
    """
    This view logs out an authenticated user by blacklisting their refresh token, effectively 
    invalidating it. The user must provide a valid refresh token in the request body. If the 
    token is valid, it is blacklisted and a success message is returned. If the token is 
    invalid, expired, or missing, an appropriate error message is returned.

    Expected Input:
    - refresh: str (required, valid refresh token)

    Returns:
    - 200 OK: On successful logout and token blacklisting
    - 400 Bad Request: If the refresh token is missing, invalid, or expired
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token :
            return Response({
                "status": "error",
                "message": "Refresh token is required."
            },status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "status": "success",
                "message": "You are successfully logged out"
            }, status=status.HTTP_200_OK) 
        
        except TokenError as e :
            return Response({
                "status": "error",
                "message": "Invalid or expired token.",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


# ------------------------- ***  End User registrations  *** -----------------------