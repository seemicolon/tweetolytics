from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns=[
    path('',views.loginUser,name='login'),
    path('logout',views.logoutUser,name='logout'),
    path('register',views.register,name='register'),
    # path('createProject',views.createProject,name='createProject'),
    path('deleteProject/<int:id>',views.deleteProject,name='deleteProject'),
    path('search',views.search,name='search'),
    # path('dashboard/(?P<pid>[\w_]+)/$',views.dashboard,name='dashboard'),
    path('dashboard/<int:id>', views.dashboard, name='dashboard'),
    # path('home',views.home,name='home'),
    path('projects',views.projects,name='projects'),
    path('compare', views.compare, name='compare'),
    path('compareproject',views.compareproject,name='compareproject'),
    path('profile',views.profile,name='profile'),
    path('reset_password/',auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),

]