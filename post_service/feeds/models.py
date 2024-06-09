from django.db import models
import uuid

# Create your models here.


class Post(models.Model):
    id = models.CharField(
        primary_key=True,
        default=uuid.uuid4().hex,
        editable=False,
        db_index=True,
        max_length=128,
    )
    user_id = models.CharField(max_length=100, default="2d3ceefdc2cd4331ba0fd9dd3fc3e3e8")
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="posts/images/", max_length=254, blank=True, null=True
    )

    def __str__(self):
        return f"{self.title}"

    def __unicode__(self):
        return 
