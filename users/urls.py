from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.SignUpView.as_view(), name='register'),
]
