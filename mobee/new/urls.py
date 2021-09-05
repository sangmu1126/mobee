from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.list, name='list'),
    path('create/', views.create, name='movie-create'),
    path('update/', views.update, name='movie-update'),
    path('detail/', views.detail, name='movie-detail'),
    path('movie/<int:id>/delete/', views.delete, name='movie-delete'),

    path('review/list/', views.review_list, name='review-list'),
    path('movie/<int:id>/', views.detail, name='movie-detail'),
    path('movie/<int:movie_id>/review/create/', views.review_create, name='review-create'),
    path('movie/<int:movie_id>/review/delete/<int:review_id>', views.review_delete, name='review-delete'),
]
