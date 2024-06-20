# movies/admin.py

from django.contrib import admin
from .models import Movie, Review, UserProfile

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(UserProfile)
