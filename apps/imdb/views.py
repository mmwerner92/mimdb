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
    url2 = "https://api.themoviedb.org/3/movie/top_rated?api_key=1a1ef1aa4b51f19d38e4a7cb134a5699&language=en-US&page=1"
    strtopmovies = requests.get(url2).content
    topmovies =  json.loads(strtopmovies)
    if 'curuser' in request.session:
        users = Users.objects.all ()
        context = {
            "curmovies":curmovies,
            "topmovies":topmovies,
            "users":users,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
    else:
        context = {
            "curmovies":curmovies,
            "topmovies":topmovies,
            "reg":"reg/",
            "label":"Log In"
        }
    return render(request,'imdb/index.html', context)

def watchlist(request):
    if 'curuser' in request.session:
        mov_list=[]
        user = Users.objects.get(id=request.session['curuser'])
        for item in user.watchlist.all():
            url = "https://api.themoviedb.org/3/movie/" + str(item.mov_id) + "?api_key=1a1ef1aa4b51f19d38e4a7cb134a5699"
            strresponse = requests.get(url).content
            movie = [json.loads(strresponse)]
            mov_list+=movie
        context = {
            "mov_list":mov_list,
            "user":user,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
    else:
        context = {
            "reg":"reg/",
            "label":"Log In"
        }
    return render(request,'imdb/watchlist.html', context)


def search(request):
    title = request.POST['search'].replace(' ', '+')
    url = "https://api.themoviedb.org/3/search/"+request.POST["search_option"]+"?api_key=1a1ef1aa4b51f19d38e4a7cb134a5699&query="+title+"&page=1"
    strresponse = requests.get(url).content
    response = json.loads(strresponse)
    if 'curuser' in request.session:
        context = {
            "response" : response,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
    else:
        context = {
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
    url = "https://api.themoviedb.org/3/movie/"+id+"?api_key=1a1ef1aa4b51f19d38e4a7cb134a5699"
    strresponse = requests.get(url).content
    movie = json.loads(strresponse)
    reviews = Review.objects.filter(movie=id)
    simurl = "https://api.themoviedb.org/3/movie/"+id+"/similar?api_key=1a1ef1aa4b51f19d38e4a7cb134a5699&language=en-US&page=1"
    strsim = requests.get(simurl).content
    simmovies = json.loads(strsim)
    movie["budget"]="{:,}".format(movie["budget"])
    movie["revenue"]="{:,}".format(movie["revenue"])
    if 'curuser' in request.session:
        context = {
            "movie":movie,
            "simmovies":simmovies,
            "reviews":reviews,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
    else:
        context = {
            "movie":movie,
            "simmovies":simmovies,
            "reviews":reviews,
            "reg":"reg/",
            "label":"Log In"
        }
    return render(request,'imdb/show.html', context)

def add_list(request, id):
    if 'curuser' in request.session:
        this_user = Users.objects.get(id=request.session['curuser'])
        if Movie.objects.filter(mov_id=id).count()<1:
            Movie.objects.create(mov_id=id)
        this_movie = Movie.objects.get(mov_id=id)
        this_user.watchlist.add(this_movie)
        return redirect('/watchlist')
    else:
        return redirect('/reg/')

def rm_list(request, id):
    if 'curuser' in request.session:
        this_user = Users.objects.get(id=request.session['curuser'])
        this_movie = Movie.objects.get(mov_id=id)
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

def result(request, search_option):
    title = request.POST['search'].replace(' ', '+')
    url = "https://api.themoviedb.org/3/search/"+search_option+"?api_key=1a1ef1aa4b51f19d38e4a7cb134a5699&query="+title+"&page=1"
    strresponse = requests.get(url).content
    response = json.loads(strresponse)
    context = {
        "response" : response,
    }
    return render(request, 'imdb/_results.html', context)
