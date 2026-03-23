from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Books


@login_required(login_url='/login/')


def books_page(request):

    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        author_name = request.POST.get('author_name')

        book_add = Books.objects.create(name=book_name, author=author_name)
        return redirect('books')

    books = Books.objects.all()
    context = {
        'book_list': books,

    }

    return render(request,'books.html',context)


@login_required(login_url='/login/')
def book_info(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    context = {
        'book': book,
    }
    return render(request, 'book_info.html', context)


