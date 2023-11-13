from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .views import GetUserView, LogoutView, RegisterView, LoginForm


urlpatterns = [
    path('social-auth/',include('social_django.urls', namespace='social')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),

]
