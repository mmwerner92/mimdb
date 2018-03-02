# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.crypto import get_random_string
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def profile(request, id):
    if 'curuser' in request.session:
        user = Users.objects.get(id=id)
        context = {
            "user":user,
            "reg":"reg/logout",
            "label":"Log Out",
            "curuser":request.session['curuser']
        }
        return render(request,'login/profile.html', context)
    else:
        return redirect('/reg/')

def update(request, id):
    errors = Users.objects.updateval(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
    else:
        user=Users.objects.get(id=id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
    return redirect('/reg/'+id)    


def logpage(request):
    if 'curuser' in request.session:
        return redirect('imdb/')
    else:
        return render(request,'login/login.html')

def regpage(request):
    if 'curuser' in request.session:
        return redirect('imdb/')
    else:
        return render(request,'login/register.html')

def register(request):
    errors = Users.objects.validate(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/reg/regpage/')
    else:
        request.session['curuser']=(Users.objects.get(email=request.POST['email'])).id
        request.session['access']='registration'
        return redirect('/')


def login(request):
    errors = Users.objects.logval(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/reg/')
    else:
        request.session['curuser']=Users.objects.filter(email=request.POST['email_login'])[0].id
        request.session['access']='login' 
        return redirect('/')


def logout(request):
    del request.session['curuser']
    del request.session['access']
    return redirect ('/')

