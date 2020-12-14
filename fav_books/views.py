from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/books')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    loggedin_user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = loggedin_user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/books')

def books(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'all_books': Book.objects.all(),
        'other_books': Book.objects.exclude(uploaded_by=request.session['user_id'])
    }
    return render(request, 'books.html', context)

def create(request):
    if request.method == 'GET':
        return redirect('/books')
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by = user,
        )
        context = {
            'book': Book.objects.last(),
            'add' : user.fav_books.add(book)
        }
        return render(request, 'onebook.html', context)

def edit(request, book_id):
        user = User.objects.get(id=request.session['user_id'])
        one_book = Book.objects.get(id=book_id)
        context = {
            'book': one_book,
            'user': user
        }
        return render(request, 'edit.html', context)

def update(request, book_id):
    if request.method == 'GET':
        return redirect('/books')
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/books/edit/{book_id}")
    else:
        User.objects.get(id=request.session['user_id'])
        to_update = Book.objects.get(id=book_id)
        to_update.title = request.POST['title']
        to_update.desc = request.POST['desc']
        to_update.save()
        updated = Book.objects.get(id=book_id)
        request.session['book_id'] = updated.id
        messages.success(request, "Book successfully updated!")
        return redirect(f"/books/{book_id}")

def onebook(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    one_book = Book.objects.get(id=book_id)
    context = {
        'book':one_book,
        'user': user
    }
    return render(request, 'onebook.html', context)

def user(request, user_id):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'all_books': Book.objects.all(),
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'user.html', context)

def others(request, user_id):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'all_books': Book.objects.all(),
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'others.html', context)

def favorite(request, book_id):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.get(id=book_id)
        user.fav_books.add(book)
        user.save()
        updated = User.objects.get(id=request.session['user_id'])
        request.session['user_id'] = updated.id
        messages.success(request, "Added to Favorite Books")
        return redirect(f'/books/{book_id}')

def unfavorite(request, book_id):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.get(id=book_id)
        user.fav_books.remove(book)
        user.save()
        updated = User.objects.get(id=request.session['user_id'])
        request.session['user_id'] = updated.id
        messages.success(request, "Removed from Favorite Books")
        return redirect(f'/books/{book_id}')


def delete(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    User.objects.get(id=request.session['user_id'])
    to_delete=Book.objects.get(id=book_id)
    to_delete.delete()
    return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect('/')
