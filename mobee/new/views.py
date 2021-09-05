from new.models import Movie, Review
from django.core.paginator import Paginator
from new.forms import MovieForm, ReviewForm, UpdateMovieForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg


def list(request):
    movies = Movie.objects.all().annotate(reviews_count=Count('review')).annotate(average_point=Avg('review__point'))
    paginator = Paginator(movies, 5)  # 한 페이지에 5개씩 표시

    page = request.GET.get('page')  # query params에서 page 데이터를 가져옴
    items = paginator.get_page(page)  # 해당 페이지의 아이템으로 필터링

    context = {
        'movies': items
    }
    return render(request, 'new/list.html', context)


def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)  # request의 POST 데이터들을 바로 PostForm에 담을 수 있습니다.
        if form.is_valid():  # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크합니다.
            new_item = form.save()  # save 메소드로 입력받은 데이터를 레코드로 추가합니다.
        return HttpResponseRedirect('/new/list/')  # 리스트 화면으로 이동합니다.
    form = MovieForm()
    return render(request, 'new/create.html', {'form': form})


def update(request):
    if request.method == 'POST' and 'id' in request.POST:
        item = get_object_or_404(Movie, pk=request.POST.get('id'))
        password = request.POST.get("password", "")
        form = UpdateMovieForm(request.POST, instance=item)
        if form.is_valid() and password == item.password:
            item = form.save()
    elif 'id' in request.GET:
        item = get_object_or_404(Movie, pk=request.GET.get('id'))
        form = MovieForm(instance=item)
        form.password = ''
        return render(request, 'new/update.html', {'form': form})

    return HttpResponseRedirect('/new/list/')  # 리스트 화면으로 이동합니다.


def detail(request, id):  # restaurant의 id (pk)를 직접 url path parameter을 통해 전달 받습니다.
    if id is not None:
        item = get_object_or_404(Movie, pk=id)
        reviews = Review.objects.filter(movie=item).all()
        return render(request, 'new/detail.html', {'item': item, 'reviews': reviews})

    return HttpResponseRedirect('/new/list/')  # 리스트 화면으로 이동합니다.


def delete(request, id):
    item = get_object_or_404(Movie, pk=id)
    if request.method == 'POST' and 'password' in request.POST:
        if item.password == request.POST.get('password'):
            item.delete()
            return redirect('list')  # 리스트 화면으로 이동합니다.

        return redirect('movie-detail', id=id)  # 비밀번호가 입력되지 않으면 상세페이지로 되돌아감

    return render(request, 'new/delete.html', {'item': item})


def review_create(request, movie_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)  #
        if form.is_valid():  # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크합니다.
            new_item = form.save()  # save 메소드로 입력받은 데이터를 레코드로 추가합니다.
        return redirect('movie-detail', id=movie_id)  # 전화면으로 이동합니다.

    item = get_object_or_404(Movie, pk=movie_id)
    form = ReviewForm(initial={'movie': item})
    return render(request, 'new/review_create.html', {'form': form, 'item':item})


def review_delete(request, movie_id, review_id):
    item = get_object_or_404(Review, pk=review_id)
    item.delete()

    return redirect('movie-detail', id=movie_id)


def review_list(request):
    reviews = Review.objects.all().select_related().order_by('-created_at')
    paginator = Paginator(reviews, 10)  # 한 페이지에 10개씩 표시

    page = request.GET.get('page')  # query params에서 page 데이터를 가져옴
    items = paginator.get_page(page)  # 해당 페이지의 아이템으로 필터링

    context = {
        'reviews': items
    }
    return render(request, 'new/review_list.html', context)
