from django.urls import path,include
from .views import RegisterView, LoginView, HomePageView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomePageView.as_view(), name='home'),
    path('chat/', include('room.urls')),
]