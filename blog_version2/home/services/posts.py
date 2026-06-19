from blog_version2.home.models import Posts
from blog_version2.users.models import BaseUser
from blog_version2.core.exceptions import ApplicationError

from django.db.models import QuerySet
from django.db import transaction
from django.utils.text import slugify

def count_post(*, user: BaseUser) -> int:
    return Posts.objects.filter(author=user).count()

@transaction.atomic
def create_post(*, user: BaseUser, title: str, content: str) ->QuerySet[Posts]:
    post = Posts.objects.create(
        author=user, title=title, content=content, slug=slugify(title)
    )
    return post

def post_update(*, slug: str, user, data: dict) -> Posts:
    post = Posts.objects.get(slug=slug)
    

    if post.author != user:
        raise ApplicationError("You are not allowed to update this post.")

    for field, value in data.items():
        setattr(post, field, value)

    post.full_clean()
    post.save(update_fields=data.keys())

    return post


def post_delete(*, slug: str, user) -> None:
    try:
        post = Posts.objects.get(slug=slug)
    except Posts.DoesNotExist:
        raise ApplicationError("Post not found.")

    if post.author != user:
        raise ApplicationError("You are not allowed to delete this post.")

    post.delete()