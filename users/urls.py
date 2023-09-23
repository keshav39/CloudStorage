from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_file, name='upload'),
    path('delete-file/<int:file_id>', views.delete_file, name='delete'),
    path('confirm_delete/', views.confirm_delete, name='confirm_delete'),
    path('share/', views.share, name='share'),
    path('manage/', views.manage, name='manage'),
    path('manage/files/', views.manage_files, name='manage_files'),
    path('manage/users/', views.manage_users, name='manage_users'),
    path('manage/delete-user/<int:user_id>/',
         views.delete_user, name='delete_user'),
    path('manage/promote-user/<int:user_id>/',
         views.promote_user, name='promote_user'),
]
