from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Article(models.Model):
	url = models.CharField(max_length=200)
	hacker_news_url = models.CharField(max_length=200)
	posted_on = models.CharField(max_length=200)
	age = models.IntegerField()
	upvotes = models.CharField(max_length=200)
	comments = models.CharField(max_length=200)
	user_read =ArrayField(models.CharField(max_length=200), default=list,blank=True)
	user_deleted =ArrayField(models.CharField(max_length=200), default=list,blank=True)