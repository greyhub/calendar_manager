from django.urls import path
from django.contrib import admin
from accounts.views import signup
from accounts.views import signin
from accounts.views import signout

app_name = 'accounts'


urlpatterns = [
    path('signup/', signup.SignUpView.as_view(), name='signup'),
    path('signin/', signin.SignInView.as_view(), name='signin'),
    path('signout/', signout.signout, name='signout'),
]