from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MoviePetition, PetitionVote
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def petition_list(request):
    petitions = MoviePetition.objects.all()
    
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    template_data['petitions'] = petitions

    return render(request, 'movies/petition_list.html', {'template_data' : template_data})

@login_required
def petition_create(request):
    if request.method == 'POST':
        movie_title = request.POST.get('movie_title', '').strip()
        description = request.POST.get('description', '').strip()
        year = request.POST.get('year', '').strip() or None
        director = request.POST.get('director', '').strip() or None

        if movie_title and description:
            petition = MoviePetition(
                movie_title = movie_title,
                description = description,
                year = int(year) if year else None,
                director = director,
                created_by=request.user
            )
            petition.save()
            messages.success(request, f'Petition for "{movie_title}" has been created successfully!')
            return redirect('movies.petition_list')
        else:
            messages.error(request, 'Movie title and description are required.')
    
    template_data = {}
    template_data['title'] = 'Create Movie Petition'

    return render(request, 'movies/petition_create.html', {'template_data': template_data})

def petition_detail(request, petition_id):
    petition = get_object_or_404(MoviePetition, id = petition_id)

    template_data = {}
    template_data['title'] = f'Petition: {petition.movie_title}'
    template_data['petition'] = petition
    template_data['user_has_voted'] = petition.has_user_voted(request.user)

    return render(request, 'movies/petition_detail.html', {'template_data': template_data})

@login_required
def petition_vote(request, petition_id):
    petition = get_object_or_404(MoviePetition, id = petition_id)

    if request.method == 'POST':
        try:
            vote = PetitionVote(petition = petition, user = request.user)
            vote.save()
            messages.success(request, f'You have successfully voted for "{petition.movie_title}"!')
        except IntegrityError:
            messages.error(request, 'You have already voted for this petition.')
    
    return redirect('movies.petition_detail', petition_id = petition_id)
        
