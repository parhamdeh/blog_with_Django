



from django.db import models
from django.core.exceptions import ValidationError
from blog_version2.common.models import BaseModel
from blog_version2.users.models import BaseUser

class Posts(BaseModel):
    slug = models.SlugField(primary_key=True, max_length=20)
    title = models.CharField(max_length=100, unique=True)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.slug
    

class Subscription(models.Model):
    subscriber = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="subs")
    target = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="targets")

    class Met:
        unique_togehter = ('subscriber', 'target')
    
    def clean(self):
        if self.subscriber == self.target:
            raise ValidationError({"subscriber": "you can't subscribe yourself."})
        
    def __str__(self):
        return f"{self.subscriber.usernme} - {self.target.username}"
