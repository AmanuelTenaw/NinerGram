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

   #path('follow/search/', views.follow_search, name='follow-search'),
   path('edit-profile/', views.edit_profile, name='edit_profile'),
  # path('profile/', views.user_profile, name='profile'),
   path('events/', views.event_list, name='event-list'),
   path('events/create/', views.create_event, name='create-event'),

    path('messages/', views.thread_list_view, name='thread-list'),
    path('messages/start/', views.start_conversation_view, name='start-conversation'),
    path('messages/<str:username>/', views.thread_detail_view, name='thread-detail'),
    path('follow/search/', views.search_users_view, name='follow-search'),

    # path('suggestions/', views.friend_suggestions, name='friend-suggestions'),

   # path('follow/<int:user_id>/', views.follow_user, name='follow-user'),
    path('search/', views.search_users_view, name='search-users'),

    path('profile/<str:username>/', views.user_profile, name='user-profile'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete-post'),

    path('followers/<str:username>/', views.followers_list, name='followers-list'),
    path('following/<str:username>/', views.following_list, name='following-list'),
    path('friend-suggestions/', views.friend_suggestions, name='friend-suggestions'),
 




    





















]
