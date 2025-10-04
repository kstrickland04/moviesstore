from django.contrib import admin

# Register your models here.

from .models import Movie, Review, MoviePetition, PetitionVote

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class MoviePetitionAdmin(admin.ModelAdmin):
    list_display = ['movie_title', 'created_by', 'status', 'vote_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['movie_title', 'created_by__username']
    readonly_fields = ['vote_count', 'created_at']
    ordering = ["-created_at"]

class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ['petition', 'user', 'voted_at']
    list_filter = ['voted_at']
    search_fields = ['petition_movie_title', 'user__username']
    ordering = ['-voted_at']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(MoviePetition, MoviePetitionAdmin)
admin.site.register(PetitionVote, PetitionVoteAdmin)