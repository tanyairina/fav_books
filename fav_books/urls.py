from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('create', views.create),
    path('books/<int:book_id>', views.onebook),
    path('books/edit/<int:book_id>', views.edit),
    path('books/update/<int:book_id>', views.update),
    path('delete/<int:book_id>', views.delete),
    path('favorite/<int:book_id>', views.favorite),
    path('unfavorite/<int:book_id>', views.unfavorite),
    path('books/user/<int:user_id>', views.user),
    path('books/others/<int:user_id>', views.others),
    path('logout', views.logout)
]
