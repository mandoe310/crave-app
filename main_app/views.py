import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Place
from django.urls import reverse_lazy
# from .forms import
# from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def places_index(request):
  places = Place.objects.all()
  return render(request, 'places/index.html', {
    'places': places
  })

def places_detail(request,place_id):
    place = Place.objects.get(id=place_id)
    return render(request,'places/detail.html',{
        'place': place,
    })

class PlaceCreate(CreateView):
    success_url = reverse_lazy('places_index')
    model = Place
    fields = ['name', 'location', 'notes', 'rating']

class PlaceUpdate(UpdateView):
    model = Place
    fields = '__all__'

class PlaceDelete(DeleteView):
    model = Place
    success_url ='/places'

    