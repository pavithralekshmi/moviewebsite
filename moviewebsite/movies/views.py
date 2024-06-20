# movies/views.py
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, MovieForm, ReviewForm
from .models import Movie, Review, UserProfile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)
            else:
                form.add_error(None, "A profile for this user already exists.")
                return render(request, 'register.html', {'form': form})
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Correctly retrieve the user
            login(request, user)    # Pass the user object to login
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect('movie_detail', movie.id)
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', movie_id)
    else:
        form = ReviewForm()
    return render(request, 'movie_detail.html', {'movie': movie, 'reviews': reviews, 'form': form})

def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == 'POST':
        movie.delete()
        return redirect('/')  # Or wherever you want to redirect after deletion
    return render(request, 'delete_confirm.html', {'movie': movie})

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    favorite_movies = user_profile.favorites.all()
    return render(request, 'profile.html', {'user_profile': user_profile, 'favorite_movies': favorite_movies})
def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})