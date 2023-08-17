from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_home, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
