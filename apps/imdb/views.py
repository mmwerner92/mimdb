# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.crypto import get_random_string
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from ..login.models import *
import bcrypt


def index(request):
    if 'curuser' in request.session:
        users = Users.objects.all ()
        context = {
            "users":users,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
    else:
        context = {
            "reg":"reg/",
            "label":"Log In"
        }
    return render(request,'imdb/index.html', context)

def watchlist(request):
    if 'curuser' in request.session:
        user = Users.objects.filter(id=request.session['curuser'])[0]
        context = {
            "user":user,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
        print user.watchlist.all()
    else:
        context = {
            "reg":"reg/",
            "label":"Log In"
        }
    return render(request,'imdb/watchlist.html', context)


def search(request):
    movies = Movie.objects.all()
    if 'curuser' in request.session:
        context = {
            "movies":movies,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
        print request.session['curuser']
        print "requested curuser"
    else:
        context = {
            "movies":movies,
            "reg":"reg/",
            "label":"Log In"
        }
    return render(request,'imdb/search.html', context)

def add(request):
    errors = Movie.objects.movalidate(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
    return redirect ('/search')

def show(request, id):
    movies = Movie.objects.filter(id=id)[0]
    reviews = Review.objects.filter(movie=Movie.objects.filter(id=id))
    if 'curuser' in request.session:
        context = {
            "movies":movies,
            "reviews":reviews,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
        print request.session['curuser']
        print "requested curuser"
    else:
        context = {
            "movies":movies,
            "reviews":reviews,
            "reg":"reg/",
            "label":"Log In"
        }
    return render(request,'imdb/show.html', context)

def add_list(request, id):
    if 'curuser' in request.session:
        this_user = Users.objects.get(id=request.session['curuser'])
        this_movie = Movie.objects.get(id=id)
        this_user.watchlist.add(this_movie)
        return redirect('/watchlist')
    else:
        return redirect('/reg/')

def rm_list(request, id):
    if 'curuser' in request.session:
        this_user = Users.objects.get(id=request.session['curuser'])
        this_movie = Movie.objects.get(id=id)
        this_user.watchlist.remove(this_movie)
        return redirect('/watchlist')
    else:
        return redirect('/reg/')

def add_review(request, id):
    if 'curuser' in request.session:
        errors = Review.objects.revvalidate(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, error)
        return redirect ('/'+id)
    else:
        return redirect('/reg/')


def rm_review(request, id, rev):
    if 'curuser' in request.session:
        Review.objects.get(id=rev).delete()
        return redirect(('/'+id))
    else:
        return redirect('/reg/')