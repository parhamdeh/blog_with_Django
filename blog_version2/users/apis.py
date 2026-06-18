from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog_version2.api.mixins import ApiAuthMixin
from blog_version2.users.serializers import RegisterInputSerializer, RegisterOutputSerializer, ProfileOutputSerializer
from blog_version2.users.selectors import get_profile
from blog_version2.users.services import register

from drf_spectacular.utils import extend_schema


class RegisterAPIView(APIView):
    """
    API endpoint for user registration.

    Accepts user credentials and profile information, creates a new user account,
    and returns the created user's public profile data.

    Authentication:
        Not required (public endpoint).

    Request Body:
        - username (str): Unique identifier for the user.
        - email (str): Valid email address.
        - password (str): Raw password (will be hashed before storage).
        - bio (str, optional): Short user biography.

    Returns:
        201 Created: Serialized user profile on success.
        400 Bad Request: Validation error or database failure.

    Example:
        POST /api/users/register/
        {
            "username": "parham",
            "email": "parham@example.com",
            "password": "StrongPass123!",
            "bio": "Django developer"
        }
    """

    @extend_schema(request=RegisterInputSerializer, responses=RegisterOutputSerializer)
    def post(self, request: Request) -> Response:
        """
        Handle POST request for user registration.

        Args:
            request (Request): DRF request object containing user registration data.

        Returns:
            Response: Serialized user data with HTTP 201 on success,
                      or error message with HTTP 400 on failure.
        """
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = register(
                username=serializer.validated_data.get("username"),
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
                bio=serializer.validated_data.get("bio"),
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=RegisterOutputSerializer(user, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class ProfileAPIView(ApiAuthMixin, APIView):
    """
    API endpoint for retrieving the authenticated user's profile.

    Returns the profile information associated with the currently
    authenticated user.

    Authentication:
        Required (see ApiAuthMixin).

    Returns:
        200 OK: Serialized profile data on success.
        401 Unauthorized: If the user is not authenticated.

    Example:
        GET /api/users/profile/
        Authorization: Bearer <token>
    """

    @extend_schema(responses=ProfileOutputSerializer)
    def get(self, request: Request) -> Response:
        """
        Handle GET request for user profile retrieval.

        Args:
            request (Request): DRF request object with authenticated user.

        Returns:
            Response: Serialized profile data with HTTP 200 on success.

        Note:
            HTTP_200_CREATED was used in the original code — corrected to HTTP_200_OK.
        """
        query = get_profile(user=request.user)

        return Response(
            data=ProfileOutputSerializer(query, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )
    

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MjM3ODA1OCwiaWF0IjoxNzgxNzczMjU4LCJqdGkiOiI5NmMxNDEzMDI1ZmQ0YzJiYTVkMjIwNDY5YzhkZjdlYyIsInVzZXJfaWQiOiIxIn0.B5hM7WYLwmx__bkadgRwM_ROsIx3fqSrjGdSPyE5fAU",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgxNzczNTU4LCJpYXQiOjE3ODE3NzMyNTgsImp0aSI6ImI3YzU1YWUyYTYzZTRjMmRiMmViNTEzZGFmYTlmYzEyIiwidXNlcl9pZCI6IjEifQ.nzJLHmXatuqxOZLf6U7iyvRQ9pCPGs1vEGLgYHwWVys"
}