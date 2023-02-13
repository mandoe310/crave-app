from django.db import models
from django.urls import reverse
from datetime import date
# from django.contrib.auth.models import User

RATING=(
    (1, '1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5')
)

# Create your models here.

class Place(models.Model):
  name = models.CharField(max_length=100)
  location = models.CharField(max_length=100)
  notes = models.TextField(max_length=2500)
  rating = models.IntegerField(
    choices=RATING,
    )
  
#   user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'place_id': self.id})
