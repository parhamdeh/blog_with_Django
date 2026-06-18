from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.serializers import RegisterInputSerializer, RegisterOutputSerializer

from drf_spectacular.utils import extend_schema


class RegisterAPIView(APIView):
    @extend_schema(request=RegisterInputSerializer, responses=RegisterOutputSerializer)
    def post(self, request:Request) -> Response:

        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = create_user(username=serializer.validated_data.get("username"),
                               email=serializer.validated_data.get("email"), 
                               password=serializer.validated_data.get("password"))
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status = status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=RegisterOutputSerializer(user, context={"request":request}).data,
            status=status.HTTP_201_CREATED
                        )


