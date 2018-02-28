# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.crypto import get_random_string
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from ..login.models import *
import bcrypt
import requests, json
from django.core import serializers


def index(request):
    url = "https://api.themoviedb.org/3/movie/now_playing?api_key=1a1ef1aa4b51f19d38e4a7cb134a5699&language=en-US&page=1&region=us"
    strcurmovies = requests.get(url).content
    curmovies = json.loads(strcurmovies)
    if 'curuser' in request.session:
        users = Users.objects.all ()
        context = {
            "users":users,
            "curmovies":curmovies,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
        print request.session['curuser']
        print "requested curuser"
    else:
        context = {
            "curmovies":curmovies,
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
    # movies = Movie.objects.all()
    title = request.POST['search'].replace(' ', '+')
    url = "https://api.themoviedb.org/3/search/"+request.POST["search_option"]+"?api_key=1a1ef1aa4b51f19d38e4a7cb134a5699&query="+title+"&page=1"
    strresponse = requests.get(url).content
    response = json.loads(strresponse)
    if 'curuser' in request.session:
        context = {
            # "movies":movies,
            "response" : response,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
    else:
        context = {
            # "movies":movies,
            "response" : response,
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

def result(request, search_option):
    title = request.POST['search'].replace(' ', '+')
    url = "https://api.themoviedb.org/3/search/"+search_option+"?api_key=1a1ef1aa4b51f19d38e4a7cb134a5699&query="+title+"&page=1"
    strresponse = requests.get(url).content
    response = json.loads(strresponse)
    context = {
        "response" : response,
    }
    return render(request, 'imdb/_results.html', context)