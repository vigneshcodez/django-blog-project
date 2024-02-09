from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
import datetime
import os

# Create your models here.


def getFileName(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s" % (now_time, filename)
    return os.path.join('uploads/', new_filename)


class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-Show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    catregory = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    videolink = models.CharField(max_length=255, null=True, blank=True)
    content = HTMLField()
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    postimage = models.ImageField(upload_to=getFileName, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


# class Websitedetails(models.Model):
#     poster = models.ImageField(upload_to=getFileName, null=True, blank=True)
#     myposterpic = models.ImageField(
#         upload_to=getFileName, null=True, blank=True)
#     mysquarepic = models.ImageField(
#         upload_to=getFileName, null=True, blank=True)
#     aboutme = HTMLField()
#     facebooklink = models.CharField(max_length=255, null=True, blank=True)
#     instagramlink = models.CharField(max_length=255, null=True, blank=True)
#     githublink = models.CharField(max_length=255, null=True, blank=True)
#     linkdinlink = models.CharField(max_length=255, null=True, blank=True)
