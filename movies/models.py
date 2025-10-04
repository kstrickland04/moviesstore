from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    
class MoviePetition(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    movie_title = models.CharField(max_length=255, help_text="Title of the movie you want to see added")
    description = models.TextField(help_text="Why should this movie be added to our catalog?")
    year = models.IntegerField(null=True, blank=True, help_text="Release year (optional)")
    director = models.CharField(max_length=255, null=True, blank=True, help_text="Director name (optional)")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_petitions')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    vote_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.movie_title} - {self.get_status_display()}"
    
    def get_vote_count(self):
        return self.petitionvote_set.count()
    
    def has_user_voted(self, user):
        if not user.is_authenticated:
            return False
        return self.petitionvote_set.filter(user=user).exists()

class PetitionVote(models.Model):
    petition = models.ForeignKey(MoviePetition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('petition', 'user')
    
    def __str__(self):
        return f"{self.user.username} voted for {self.petition.movie_title}"