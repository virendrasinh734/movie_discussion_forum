from django.urls import path
from . import views

urlpatterns=[
    path('login/', views.login_page,name="login"),
    path('logout/', views.logout_user,name="logout"),
    path('register/', views.register_page,name="register"),
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='room'),
    path('create-room/',views.create_room,name='create-room'),
    path('update-room/<str:pk>',views.update_room,name='update-room'),
    path('delete-room/<str:pk>',views.delete_room,name='delete-room'),
    path('delete-message/<str:pk>',views.delete_message,name='delete-message'),
    path('profile/<int:pk>',views.user_profile,name='user-profile'),
    path('rate-movie/<int:pk>/', views.rate_movie, name='rate-movie'),
    path('myprofile/', views.my_profile, name='myprofile'),
    path('rec/', views.rec, name='rec')
]