from django.db import models


# Create your models here.
# 상속
# 상속 받고자하는 다른 class 를 ()괄호 안에 넣어준다.
class Board(models.Model):

    # 클래스 변수 -> DB 의 필드를 나타냄.
    # id 는 기본적으로 처음 테이블 생성시 자동으로 만들어진다. 그래서 아래와 같이 만들어도 되고 안 만들어도 된다.
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)  # 길이의 문자열을 제한할 때 쓴다.  # CharField 괄호 안에 max_length=0 가 필수로 있어야 한다.
    writer = models.CharField(max_length=10)  # 길이의 문자열을 제한할 때 쓴다.  # CharField 괄호 안에 max_length=0 가 필수로 있어야 한다.
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add : '객체를 하나 생성할 때만 시간을 담겠다' 라는 의미
    updated_at = models.DateTimeField(auto_now=True)  # auto_now : 지금 작업을 할 때


    # 인스턴스 그 자체 형식을 어떻게 출력할지 정하는 class method 다
    def __str__(self):
        return f'{self.id}번째 글ㅤㅤ ㅤㅤ ㅤㅤ {self.title} : {self.content}'


# 상속 받고자하는 다른 class 를 ()괄호 안에 넣어준다.
class Comment(models.Model):
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add : '객체를 하나 생성할 때만 시간을 담겠다' 라는 의미
    updated_at = models.DateTimeField(auto_now=True)  # auto_now : 지금 작업을 할 때
    # 일(게시판) 대 다(댓글들) 관계 이기 때문에 foreign key 설정을 해줘야한다.
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    # 게시판이 삭제 될 때 댓글들 처리 옵션은 아래와 같다.
    # Board, on_delete=models.CASCADE -> Board 게시판 삭제하면 댓글들도 다 삭제
    # Board, on_delete = models.SET_NULL --> Board 게시판 삭제하면 댓글들 널 처리
    # Board, on_delete = models.Do.NOTHING -> Board 게시판 삭제하면 댓글을은 아무 처리도 하지 마세요.