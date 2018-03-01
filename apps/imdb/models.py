# Inside models.py
from __future__ import unicode_literals
from django.db import models
from ..login.models import *
import re, bcrypt
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
IMG_URL_REGEX = re.compile(r'^(http|https)://')
NAME_REGEX = re.compile(r'^[a-zA-Z]+" "+[a-zA-Z]$')


class MovManager(models.Manager):
    def movalidate(self, post_data):
        errors = []
        if len(post_data['mov_title']) < 1:
            errors.append("Movie must have a title!")
        if len(post_data['mov_img']) < 1:
            errors.append("Please include a proper url!")
        elif not IMG_URL_REGEX.match((post_data['mov_img'])):
            errors.append("Invalid image URL!")            
        if not (post_data['mov_release']):
            errors.append("Please include a release date!")
        if len(post_data['mov_director']) < 1:
            errors.append("Please add a director!")
        if len(post_data['mov_descript']) < 1:
            errors.append("Please add a description!")        
        if (Movie.objects.filter(mov_title=post_data['mov_title']).count()>0):
            errors.append("That movie is already in our database!")
        if not len(errors):
            Movie.objects.create(
            mov_title=post_data['mov_title'],
            mov_img=post_data['mov_img'],
            mov_release=post_data['mov_release'],
            mov_director=post_data['mov_director'],
            mov_descript=post_data['mov_descript'])
        return errors    

class RevManager(models.Manager):
    def revvalidate(self, post_data):
        errors = []
        if len(post_data['rev_text']) < 1:
            errors.append("Please add some text!")     
        if (Review.objects.filter(movie=post_data['movie'], reviewer=Users.objects.get(id=post_data['curuser'])).count()>0):
            errors.append("You have already left a review for this film!")
        if not len(errors):
            Review.objects.create(
            rev_text=post_data['rev_text'],
            rev_score=post_data['rev_score'],
            reviewer=Users.objects.get(id=post_data['curuser']),
            movie=post_data['movie'])
        return errors    


class Movie(models.Model):
    mov_id = models.IntegerField()
    watchlist = models.ManyToManyField(Users, related_name="watchlist")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Review(models.Model):
    rev_text = models.TextField()
    rev_score = models.IntegerField()
    reviewer = models.ForeignKey(Users, related_name="user_review")
    movie = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = RevManager()