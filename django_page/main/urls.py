from django.urls import path, include
from . import views
import comment.views 
urlpatterns = [
    path('', views.index, name = 'index'),
    path('landing/', views.landing),
    path('comment/', include('comment.urls'))
]