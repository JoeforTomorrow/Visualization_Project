from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET
from .models import Board


# Create your views here
# @require_GET  # GET 요청만 들어오게 만들 수 있다.
def index(request):
    # Board 의 전체 데이터를 불러온다 - QuerySet
    boards = Board.objects.all()
    context = {'boards': boards}
    return render(request, 'boards/index.html', context)


# RESTful 후
# 사용자 입력을 받는 페이지 렌더링
# @require_http_methods(['GET', 'POST'])
def new(request):
    # GET 사용자가 작성할 수 있는 게시글을 달라라는 행위
    # POST 사용자가 게시글을 작성하겠다라는 행위
    print(request.method)  # new.html 에 가면 GET 인지 POST 인지 확인 할 수 있음. GET 임

    # GET
    if request.method == 'GET':
        return render(request, 'boards/new.html')
    # POST
    else:
        print(request.method)  # new.html 에 가서 새로 글을 작성하면 GET 인지 POST 인지 확인 할 수 있음. POST 임
        title = request.POST.get('title')  # 사용자가 POST 로 보낸 걸 get 가져오기
        content = request.POST.get('content')  # 사용자가 POST 로 보낸 걸 get 가져오기
        board = Board(title=title, content=content)
        board.save()
        return redirect('boards:detail', board.id)



# RESTful 후
# 특정 게시글 하나만 가지고 온다.
def detail(request, board_id):
    # Board 클래스를 사용해서 id 값에 맞는 데이터를 가지고 온다.
    # context 로 넘겨서 detail.html 페이지에서 title 과 content 를
    # 출력해본다.
    board = get_object_or_404(Board, id=board_id)
    context = {'board': board}
    return render(request, 'boards/detail.html', context)



# RESTful 처리 후 # require_http_methods 처리 후
@require_http_methods(['POST'])
# 허락할 것만 리스트에 담는다. ['POST', 'GET'] 이렇게 쓸 수 있음.
# POST 만 오게끔 설정했는데 GET 이 오면 url에 HTTP ERROR 405 뜬다.
# 콘솔창에는 Method Not Allowed (GET): /boards/5/delete/
# [11/Jun/2019 15:27:49] "GET /boards/5/delete/ HTTP/1.1" 405 0 뜬다.
def delete(request, board_id):
    # if request.method == 'GET':
    #     # GET 요청으로 들어오면 detail page 로 다시 redirect
    #     return redirect('boards:detail', id)  # boards:detail 콜론에 띄어쓰기가 있으면 안됨.
    # else:
        # POST 요청으로 들어오면 정상 삭제
        board = Board.objects.get(id=board_id)
        board.delete()
        return redirect('boards:index')



# RESTful 후
# 게시글 수정 페이지 렌더링
def edit(request, board_id):
    # 0. Board 클래스를 통해 id 값에 맞는 데이터를 가져온다.
    # board = Board.objects.get(id=id)  # DRY : Don't repeat yourself
    board = get_object_or_404(Board, id=board_id)

    # 1. 사용자의 요청이 GET 인지 POST 인지 확인한다.
    if request.method == 'GET':
        # 2. GET 요청이면 사용자에게 수정할 페이지를 보여준다.
        context = {'board': board}
        return render(request, 'boards/edit.html', context)
    else:
        # 3. POST 요청이면 사용자가 보낸 데이터를 받아서 수정한 뒤 detail page 로 redirect 한다.
        title = request.POST.get('title')  # 사용자가 POST 로 보낸 걸 get 가져오기
        content = request.POST.get('content')  # 사용자가 POST 로 보낸 걸 get 가져오기
        # id 값에 맞는 board 데이터를 위에서 주어진 title 과 content 에 맞게 수정한 뒤 저장하는 로직
        # 해당 데이터의 내용을 주어진 title, content 로 수정한다.
        board.title = title
        board.content = content
        # 저장한다.
        board.save()
        return redirect('board:detail', board_id)  # 주의! boards:detail 콜론에 띄어쓰기가 있으면 안됨.


# Create your views here.
# RESTful 후
# 특정 게시글 하나만 가지고 온다.
def detail(request, board_id):
    # Board 클래스를 사용해서 id 값에 맞는 데이터를 가지고 온다.
    # context 로 넘겨서 detail.html 페이지에서 title 과 content 를
    # 출력해본다.
    board = get_object_or_404(Board, id=board_id)
    comments = board.comment_set.order_by('-id').all()  # id의 역순으로 댓글 순서 정렬
    context = {'board': board, 'comments': comments}
    return render(request, 'boards/detail.html', context)


def comment_create(request, board_id):
    # 댓글 생성하는 로직
    content = request.POST.get('content')
    comment = Comment()
    comment.board_id = board_id
    comment.content = content
    comment.save()

    return redirect('boards:detail', board_id)