from django.db import models
from django.contrib.auth.models import AbstractUser
from . import validators

# 사용자 모델
class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        validators=[validators.validate_no_special_characters],
        error_messages={"unique": "이미 사용 중입니다."},
    )

    prefer = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.email)

# 영화 모델
class Movie(models.Model):
    movie_id = models.CharField(max_length=30, primary_key=True)
    movie_title = models.CharField(max_length=100)
    release_year = models.CharField(max_length=4)
    poster_img = models.TextField()
    director = models.CharField(max_length=30)
    summary = models.TextField()

    class Meta:
        ordering = ['release_year']

    def __str__(self):
        return f'{self.movie_title} - {self.release_year}'
    

class MovieRating(models.Model):
    rating = models.FloatField()
    movies = models.OneToOneField(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rating)
    

class Genres(models.Model):
    genres = models.CharField(max_length=30)

    movies = models.ManyToManyField(Movie)
    
    def __str__(self):
        return str(self.movies)
    

class TempPrefer(models.Model):
    iid = models.CharField(max_length=30)
    title = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    rating_avg = models.FloatField()
    poster = models.TextField()
    genres = models.CharField(max_length=100)
    director = models.CharField(max_length=50)
    summary = models.TextField()

    def __str__(self):
        return f'{self.title} - {self.year} - {self.genres}'