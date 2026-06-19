from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from yaml import serialize

from blog_version2.home.services.posts import create_post, post_delete, post_update
from blog_version2.home.selectors.posts import post_list, post_detail
from blog_version2.api.mixins import ApiAuthMixin
from blog_version2.api.pagination import LimitOffsetPagination, get_paginated_response_context
from blog_version2.home.serializers.posts import FilterPostSerializer, PostDetailOutputSerializer, PostInputSerializer, PostOutputSerializer

from drf_spectacular.utils import extend_schema




class PostAPIView(ApiAuthMixin, APIView):
    """
    API endpoint for creating and listing posts.

    Features:
    - Create a new post for the authenticated user.
    - Retrieve posts from subscribed authors.
    - Support filtering and pagination.
    """
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        request=PostInputSerializer,
        responses=PostOutputSerializer,
        )
    def post(self, request:Request) -> Response:
        """
        Create a new post.

        Creates a post owned by the authenticated user and
        returns the serialized post data.

        Returns:
            201 Created:
                Post successfully created.

            400 Bad Request:
                Validation or database error.
        """
        serializer = PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            post = create_post(
                user=request.user,
                content=serializer.validated_data.get("content"),
                title = serializer.validated_data.get("title"),
            )
        except Exception as ex:
            return Response(
                {"detail":"Database Error -" + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        return Response(
            data=PostOutputSerializer(post, context={"request":request}).data,
            status=status.HTTP_201_CREATED,
            )
    
    @extend_schema(
        parameters=[FilterPostSerializer],
        responses=PostOutputSerializer,
        )
    def get(self, request:Request) -> Response:
        """
        List posts visible to the authenticated user.

        Retrieves posts from subscribed users and optionally
        applies filtering and pagination.

        Supported filters:
        - title
        - slug
        - search
        - author__in
        - created_at__range

        Returns:
            200 OK:
                Paginated list of posts.

            400 Bad Request:
                Invalid filter parameters or database error.
        """
        filter_serializer = FilterPostSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        try:
            posts = post_list(
                filters = filter_serializer.validated_data, user=request.user
            )
        except Exception as ex:
            return Response(
                {"detail":"Database Error -" + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=PostOutputSerializer,
            queryset=posts,
        )
        
class PostRetrievUpdateDestroy(ApiAuthMixin, APIView):
    """
    API endpoint for retrieving, updating, and deleting a specific post.

    All actions require authentication and ownership of the post.

    Authentication:
        Required — JWT Bearer token.

    URL Parameters:
        slug (str): The unique slug identifier of the post.
    """

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(responses=PostDetailOutputSerializer)
    def get(self, request: Request, slug: str) -> Response:
        """
        Retrieve details of a specific post by slug.

        Args:
            request (Request): DRF request object with authenticated user.
            slug (str): Unique slug of the post to retrieve.

        Returns:
            Response:
                - 200 OK: Serialized post detail data.
                - 400 Bad Request: Post not found or database error.

        Example:
            GET /api/posts/my-post-slug/
            Authorization: Bearer <token>
        """
        try:
            post = post_detail(
                slug=slug,
                user=request.user,
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            PostDetailOutputSerializer(post, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=PostInputSerializer,
        responses=PostDetailOutputSerializer,
    )
    def patch(self, request: Request, slug: str) -> Response:
        """
        Partially update a specific post by slug.

        Only the post author can update their own post.
        All fields are optional — only provided fields will be updated.

        Args:
            request (Request): DRF request object with authenticated user.
            slug (str): Unique slug of the post to update.

        Request Body (all optional):
            - title (str): New title for the post (max 100 chars).
            - content (str): New content for the post (max 1000 chars).

        Returns:
            Response:
                - 200 OK: Serialized updated post data.
                - 400 Bad Request: Validation error or database error.
                - 403 Forbidden: User is not the author of the post.

        Example:
            PATCH /api/posts/my-post-slug/
            Authorization: Bearer <token>
            {
                "title": "Updated Title"
            }
        """
        serializer = PostInputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            post = post_update(
                slug=slug,
                user=request.user,
                data=serializer.validated_data,
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            PostDetailOutputSerializer(post, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(responses=None)
    def delete(self, request: Request, slug: str) -> Response:
        """
        Delete a specific post by slug.

        Only the post author can delete their own post.
        This action is irreversible.

        Args:
            request (Request): DRF request object with authenticated user.
            slug (str): Unique slug of the post to delete.

        Returns:
            Response:
                - 204 No Content: Post successfully deleted.
                - 400 Bad Request: Post not found or database error.
                - 403 Forbidden: User is not the author of the post.

        Example:
            DELETE /api/posts/my-post-slug/
            Authorization: Bearer <token>
        """
        try:
            post_delete(
                slug=slug,
                user=request.user,
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)