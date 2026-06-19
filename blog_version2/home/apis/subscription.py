from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from blog_version2.api.mixins import ApiAuthMixin
from blog_version2.home.services.subscription import unsubscribe, subscribe
from blog_version2.home.selectors.subscription import get_subscribers
from blog_version2.api.pagination import LimitOffsetPagination, get_paginated_response_context
from blog_version2.home.serializers.subscription import SubscribeInputSerializer, SubscribeOutputSerializer

from drf_spectacular.utils import extend_schema


class SubscribeDtailAPIView(ApiAuthMixin, APIView):
    """
    API endpoint for managing a specific subscription relationship.

    Allows an authenticated user to unsubscribe from another user
    identified by their username.

    Authentication:
        Required — JWT Bearer token.

    URL Parameters:
        username (str): The username of the user to unsubscribe from.
    """

    def delete(self, request: Request, username: str) -> Response:
        """
        Unsubscribe the authenticated user from the specified user.

        Args:
            request (Request): DRF request object with authenticated user.
            username (str): Username of the user to unsubscribe from.

        Returns:
            Response:
                - 204 No Content: Successfully unsubscribed.
                - 400 Bad Request: Database or business logic error.

        Example:
            DELETE /api/subscriptions/parham/
            Authorization: Bearer <token>
        """
        try:
            unsubscribe(user=request.user, username=username)
        except Exception as ex:
            return Response(
                {"detail": "Database Error -" + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeAPIView(ApiAuthMixin, APIView):
    """
    API endpoint for listing and creating subscriptions.

    Supports:
        - GET: Retrieve a paginated list of subscribers for the authenticated user.
        - POST: Subscribe the authenticated user to another user.

    Authentication:
        Required — JWT Bearer token.

    Pagination:
        Uses LimitOffset pagination with a default limit of 10 results per page.

    Query Parameters (GET):
        - limit (int): Number of results per page (default: 10).
        - offset (int): Starting position in the result set (default: 0).
    """

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(responses=SubscribeOutputSerializer)
    def get(self, request: Request) -> Response:
        """
        Retrieve a paginated list of subscribers for the authenticated user.

        Args:
            request (Request): DRF request object with authenticated user.

        Returns:
            Response:
                - 200 OK: Paginated list of subscribers.
                - 401 Unauthorized: If the user is not authenticated.

        Example:
            GET /api/subscriptions/?limit=10&offset=0
            Authorization: Bearer <token>
        """
        query = get_subscribers(user=request.user)

        return get_paginated_response_context(
            request=request,
            pagination_class=self.Pagination,
            queryset=query,
            serializer_class=SubscribeOutputSerializer,
            view=self,
        )

    @extend_schema(
        request=SubscribeInputSerializer,
        responses=SubscribeOutputSerializer,
    )
    def post(self, request: Request) -> Response:
        """
        Subscribe the authenticated user to another user.

        Args:
            request (Request): DRF request object with authenticated user.

        Request Body:
            - username (str): Username of the user to subscribe to.

        Returns:
            Response:
                - 200 OK: Serialized subscription data on success.
                - 400 Bad Request: Database or business logic error
                  (e.g. already subscribed, user not found, self-subscription).
                - 401 Unauthorized: If the user is not authenticated.

        Example:
            POST /api/subscriptions/
            Authorization: Bearer <token>
            {
                "username": "parham"
            }
        """
        serializer = SubscribeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = subscribe(
                user=request.user,
                username=serializer.validated_data.get("username"),
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error -" + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(SubscribeOutputSerializer(query).data)