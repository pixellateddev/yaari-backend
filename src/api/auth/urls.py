from django.urls import path
from .views import Login, Logout, RefreshToken

urlpatterns = [
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('refresh/', RefreshToken.as_view())
]
