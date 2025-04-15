from django.urls import path
from . import views


urlpatterns = [
   path('login/', views.loginPage, name = "login"),
   path('logout/', views.logoutUser, name = "logout"),
   path('register/', views.registerPage, name = "register"),
   path('post/create/', views.create_post, name='create-post'),
   path('', views.main_view, name='home'),     
   path('rooms/', views.home, name='rooms-home'),
   path('follow/<int:user_id>/', views.follow_user, name='follow-user'),
   path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow-user'),
   path('follow/search/', views.follow_search, name='follow-search'),




]
