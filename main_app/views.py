import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from .models import Place
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Place, Photo

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def places_index(request):
  places = Place.objects.filter(user=request.user)
  return render(request, 'places/index.html', {
    'places': places
  })

@login_required
def places_detail(request, place_id):
    place = Place.objects.get(id=place_id)
    return render(request,'places/detail.html',{
        'place': place,
    })

class PlaceCreate(LoginRequiredMixin, CreateView):
    model = Place
    fields = ['name', 'location', 'notes', 'rating']

    def form_valid(self, form):
     form.instance.user = self.request.user  
     return super().form_valid(form)

class PlaceUpdate(LoginRequiredMixin, UpdateView):
    model = Place
    fields = '__all__'

class PlaceDelete(LoginRequiredMixin, DeleteView):
    model = Place
    success_url ='/places'

@login_required
def add_photo(request, place_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, place_id=place_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', place_id=place_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


    