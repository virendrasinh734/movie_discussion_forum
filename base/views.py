from django.shortcuts import render, redirect
from django.db.models import Avg

from django.db.models import Q
# Create your views here.
from django.http import HttpResponse
from .models import Movie, Topic, Message, Rating
from .forms import RoomForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from dotenv import load_dotenv
load_dotenv() ## load

import os
import streamlit as st
import google.generativeai as genai

from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.llms import gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import SimpleDirectoryReader
# rooms=[
#     {'id': 1, 'name': 'Bridge of Spies'},
#     {'id': 2, 'name': 'Inception'},
#     {'id': 3, 'name': 'Oppenheimer'}
# ]

def login_page(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User with that Username does not exist')
        user=authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')
    context={'page':page}
    return render(request, 'login_register.html',context)

def logout_user(request):
    logout(request)
    return redirect('home')
def register_page(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Error occured during registration")
    return render(request, 'login_register.html',{'form': form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Movie.objects.filter(Q(topic__name__icontains=q)|
                               Q(name__icontains=q)|
                               Q(description__icontains=q))
    topics=Topic.objects.all()
    room_count=rooms.count()
    room_messages=Message.objects.all().order_by('-created')
    context={'rooms':rooms, 'topics': topics,
             'room_count':room_count,'room_messages':room_messages}
    return render(request,'home.html',context)

def room(request,pk):
    room=Movie.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('created')
    participants=room.particpants.all()
    ratings = Rating.objects.filter(movie=room)
    
    # Calculate aggregate ratings
    aggregate_ratings = {
        'acting': ratings.aggregate(avg_acting=Avg('acting')).get('avg_acting', None),
        'plot': ratings.aggregate(avg_plot=Avg('plot')).get('avg_plot', None),
        'cinematography': ratings.aggregate(avg_cinematography=Avg('cinematography')).get('avg_cinematography', None),
        'theme': ratings.aggregate(avg_theme=Avg('theme')).get('avg_theme', None),
        'dialogue': ratings.aggregate(avg_dialogue=Avg('dialogue')).get('avg_dialogue', None),
        'characters': ratings.aggregate(avg_characters=Avg('characters')).get('avg_characters', None),
        'overall': ratings.aggregate(avg_overall=Avg('overall')).get('avg_overall', None),
    }
    
    
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.particpants.add(request.user)
        return redirect('room',pk=room.id)
    context = {
        'room': room,
        'messages': room_messages,
        'participants': participants,
        'aggregate_ratings': aggregate_ratings
    }
    return render(request,'room.html',context)

@login_required(login_url='/login')
def create_room(request):
    form= RoomForm()
    if request.method =='POST':
        # print(request.POST)
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')
    context={'form':form}
    return render(request,'movie_form.html', context)

@login_required(login_url='/login')
def update_room(request,pk):
    room=Movie.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.method =='POST':
        # print(request.POST)
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'movie_form.html', context)

@login_required(login_url='/login')
def delete_room(request,pk):
    room=Movie.objects.get(id=pk)
    if request.method== 'POST':
        room.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj': room})
@login_required(login_url='/login')
def delete_message(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!= message.user:
        return HttpResponse("yOU ARE NOT ALLOWED TO DELETE")
    
    message.delete()
    return redirect('home')
    return render(request,'delete.html',{'obj': message})

def user_profile(request,pk):
    user=User.objects.get(pk=pk)
    rooms=user.movie_set.all()
    room_message=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user, 'rooms': rooms,'room_messages':room_message,'topics':topics}
    return render(request, 'profile.html',context)

def my_profile(request):
    print(request.user.id)
    user=User.objects.get(request.user.id)
    rooms=user.movie_set.all()
    room_message=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user, 'rooms': rooms,'room_messages':room_message,'topics':topics}
    return render(request, 'profile.html',context)

@login_required(login_url='/login')
def rate_movie(request, pk):
    if request.method == 'POST':
        acting = int(request.POST.get('acting'))
        plot = int(request.POST.get('plot'))
        cinematography = int(request.POST.get('cinematography'))
        theme = int(request.POST.get('theme'))
        dialogue = int(request.POST.get('dialogue'))
        characters = int(request.POST.get('characters'))
        overall = int(request.POST.get('overall'))

        movie = Movie.objects.get(id=pk)
        user = request.user

        # Check if the user has already rated this movie
        existing_rating = Rating.objects.filter(user=user, movie=movie).first()
        if existing_rating:
            messages.error(request, 'You have already rated this movie.')
        else:
            Rating.objects.create(
                user=user,
                movie=movie,
                acting=acting,
                plot=plot,
                cinematography=cinematography,
                theme=theme,
                dialogue=dialogue,
                characters=characters,
                overall=overall
            )
            messages.success(request, 'Thank you for rating this movie.')

    return redirect('room', pk=pk)

def rec(request):
    if request.method == 'POST':
        question = request.POST.get('movie', '')  # Get the movie name from the form
        genai.configure(api_key="")  
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        q=f"Suggest 5 movies similar to {question}" 
        responses = chat.send_message(q, stream=True)
        text_response=[]
        for chunk in responses:
            text_response.append(chunk.text)
        a= "".join(text_response)
        movie_names = extract_movie_names(a)
        print(movie_names)
        context = {'movie_names': movie_names}
        return render(request, 'recommend.html', context)
    return render(request, 'recommend.html')



import re

def extract_movie_names(text):
    pattern = r'\*\*(.*?)\*\*'
    matches = re.findall(pattern, text)
    return matches

# text = "1. **Memento (2000)**: A psychological thriller about a 2. **The Shawshank Redemption (1994)**: A gripping drama..."
