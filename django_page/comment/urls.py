from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.comment, name = "comment"),
    path('createComment/', views.createComment, name = "createComment"),
    path('deleteComment/', views.deleteComment, name = 'deleteComment')
]