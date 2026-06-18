from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from blog_version2.api.mixins import ApiAuthMixin
from users.serializers import RegisterInputSerializer, RegisterOutputSerializer, ProfileOutputSerializer
from users.selectors import get_profile
from users.services import register

from drf_spectacular.utils import extend_schema

 

class RegisterAPIView(APIView):
    @extend_schema(request=RegisterInputSerializer, responses=RegisterOutputSerializer)
    def post(self, request:Request) -> Response:

        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = register(username=serializer.validated_data.get("username"),
                               email=serializer.validated_data.get("email"), 
                               password=serializer.validated_data.get("password"),
                               bio = serializer.validated_data.get("bio"),
                               )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status = status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=RegisterOutputSerializer(user, context={"request":request}).data,
            status=status.HTTP_201_CREATED
                        )
    

class ProfileAPIView(APIView):
    @extend_schema(responses=ProfileOutputSerializer)
    def get(self, request:Request) -> Response:

        query = get_profile(user=request.user)

        return Response(
            data=ProfileOutputSerializer(query, context={"request":request}, many=True).data,
            status=status.HTTP_200_CREATED
                    )


