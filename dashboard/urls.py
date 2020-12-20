from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns=[
    path('login',views.loginUser,name='login'),
    path('logout',views.logoutUser,name='logout'),
    path('register',views.register,name='register'),
    path('createProject',views.createProject,name='createProject'),
    path('search',views.search,name='search'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('home',views.home,name='home'),
    path('projects',views.projects,name='projects'),
    path('profile',views.profile,name='profile'),
    path('reset_password/',auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),

]