from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

RATING=(
    (0,''),
    (1, '⭐️'),
    (2,'⭐️⭐️'),
    (3,'⭐️⭐️⭐️'),
    (4,'⭐️⭐️⭐️⭐️'),
    (5,'⭐️⭐️⭐️⭐️⭐️')
)


TYPES =(
  ('R','restaurant'),
  ('C','cafe'),
  ('B','bar'),
  ('D', 'dessert'),
)

STATUS = (
  ('B','Been'),
  ('H','Have not been'),
)
# Create your models here.

class Place(models.Model):
  name = models.CharField(max_length=100)
  location = models.CharField(max_length=100)
  status = models.CharField(
    max_length=1,
    choices=STATUS,
  )
  notes = models.TextField(
    max_length=2500,
    blank=True,
    )
  place_type = models.TextField(
    choices=TYPES,
  )
  rating = models.IntegerField(
    choices=RATING,
    default=0
    )
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'place_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for place_id: {self.place_id} @{self.url}"


