from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.bloghome, name='bloghome'),
    path('<str:slug>/', views.blogPost, name='blogPost'),

    # API to post a comment
    path('postComment', views.postComment, name='postComment')
]