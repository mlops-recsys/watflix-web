from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Movie, MovieRating, Genres, User
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Movie)
admin.site.register(MovieRating)
admin.site.register(Genres)