from django.urls import path
from . import views


app_name = 'boards'


urlpatterns = [
    path('', views.index, name='index'),  # www.web.com/boards/
    path('new/', views.new, name='new'),  # 사용자의 입력을 받아서 게시글을 작성하는 곳
    # path('create/', views.create, name='create'),  # 사용자가 입력한 데이터를 전송받고 실제 DB에 작성 및 사용자 피드백
    path('<int:board_id>/', views.detail, name='detail'),  # www.web.com/boards/<id>/
    path('<int:board_id>/delete/', views.delete, name='delete'),
    path('<int:board_id>/edit/', views.edit, name='edit'),  # 게시글 수정 페이지 렌더링
    # path('<int:board_id>/update/', views.update, name='update'),  # 사용자가 입력한 수정 데이터를 전송 받고 실제 DB 에 수정 후 저장


    # Comments
    path('<int:board_id>/comments/', views.comment_create, name='comment_create'),
    path('<int:board_id>/comments/<int:comment_id>/delete', views.comment_delete, name='comment_delete'),
]