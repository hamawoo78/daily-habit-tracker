from django.urls import path
from . import views

urlpatterns = [
    path('', views.habits_tracker, name='habits_tracker'),
    path('history/', views.mood_history, name='mood_history'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
]