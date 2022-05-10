from time import time
from django.shortcuts import get_object_or_404, redirect, render
from .models import Board
from django.utils import timezone
# Create your views here.
def home(request):
    boards = Board.objects.all()
    return render(request, 'board/home.html', {'boards':boards})

def new(request):
    return render(request, 'board/new.html')

def detail(request, id):
    board = get_object_or_404(Board, pk = id)
    return render(request, 'board/detail.html',{'board':board})

def create(request):
    new_board = Board()
    new_board.title = request.POST['title']
    new_board.writer = request.POST['writer']
    new_board.body = request.POST['body']
    new_board.pub_date = timezone.now()
    new_board.save()
    return redirect('detail',new_board.id)

def edit(request, id):
    edit_board = Board.objects.get(id=id)
    return render(request, 'board/edit.html',{'board':edit_board})

def update(request, id):
    update_board = Board.objects.get(id=id)
    update_board.title = request.POST['title']
    update_board.writer = request.POST['writer']
    update_board.body = request.POST['body']
    update_board.pub_date = timezone.now()
    update_board.save()
    return redirect('detail',update_board.id)

def delete(request, id):
    delete_board = Board.objects.get(id = id)
    delete_board.delete()
    return redirect('home')