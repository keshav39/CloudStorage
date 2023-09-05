from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_file, name='upload'),
    path('delete/<int:file_id>', views.delete_file, name='delete'),
    path('share/', views.share, name='share'),
    path('manage/files/', views.manage_files, name='manage_files'),
    # path('manage/users/', views.manage_users, name='manage_users'),
]
