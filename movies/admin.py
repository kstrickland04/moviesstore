from django.contrib import admin

# Register your models here.

from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin):
    ordering = ["name"]
    search_fields = ["name"]
    list_display = ("id", "name", "stock", "price")
    list_editable = ("stock", "price")
    list_filter = ("stock",)   

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)