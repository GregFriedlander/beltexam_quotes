from __future__ import unicode_literals 
import bcrypt
from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages 
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, "quote_wall/logreg.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.validate_reg(request.POST)
        if len(errors):
            for key in errors:
                messages.error(request, errors[key])
            return redirect('/')
    
    pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=pw, birthdate=request.POST['birthdate'])
    request.session['id'] = user.id
    request.session['name'] = user.name
    request.session['alias'] = user.alias
    request.session['email'] = user.email
    return redirect('/homepage')

def login(request):
    login_return = User.objects.validate_login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        request.session['name'] = login_return['user'].name
        request.session['alias'] = login_return['user'].alias
        request.session['email'] = login_return['user'].email
        
        return redirect('/homepage')
    else:
        messages.error(request, login_return['error'])
        return redirect('/')

def homepage(request):
    quotes = Quote.objects.exclude(favorites=request.session['id'])
    me = User.objects.get(id=request.session['id'])
    fav_quotes = me.fav_quotes.all()
    
    context = {
        "quotes": quotes,
        "fav_quotes": fav_quotes
    }
    return render(request, "quote_wall/homepage.html", context)

def processquote(request):
    if len(request.POST['quoted_by']) < 3:
        messages.error(request, "Quoted By Field must be more that 3 characters")
        return redirect('/homepage')
    if len(request.POST['message']) < 10:
        messages.error(request, "Message Field must be at least 10 characters")
        return redirect('/homepage')
    else:
        creator = User.objects.get(id=request.session['id'])
        Quote.objects.create(quoted_by=request.POST['quoted_by'], message=request.POST['message'], creator=creator)
        return redirect('/homepage')

def addfavorite(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=request.session['id'])
    quote.favorites.add(user)
    return redirect('/homepage')

def removefavorite(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=request.session['id'])
    quote.favorites.remove(user)
    return redirect('/homepage')
    
def userpage(request, user_id):
    user = User.objects.get(id=user_id)
    quotes = user.quotes.all()
    print "This is the length"
    context = {
        "user": user,
        "quotes": quotes
    }
    return render(request, "quote_wall/userpage.html", context)

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')