from django.db import models
from django.template.defaultfilters import slugify

from django.utils import timezone
from users.models import User

# Create your models here.
class Post(models.Model):

    DRAFT = "Draft"
    ARCHIVED = 'Archived'
    PUBLISHED = 'Published'

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (ARCHIVED, 'Archived'),
        (PUBLISHED, 'Published')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    cover = models.ImageField(upload_to='cover', default='/default/cover.jpg')
    status = models.CharField(max_length=25, default=DRAFT, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

