from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from movies.models import Movie
from django.core.exceptions import ValidationError

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.user.username

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    
    def buy(self):
        if self.movie.stock < self.quantity:
            raise ValidationError(f"Not enough stock for {self.movie.name}")
        self.movie.stock -= self.quantity
        self.movie.refresh_from_db()