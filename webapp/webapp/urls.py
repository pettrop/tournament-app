"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path

import accounts.views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/signup/', accounts.views.SignUpView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name="registration/password_change.html"), name='password_change'),
    path('accounts/password_change/done', PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"), name='password_change_done'),
    path('accounts/signup_successful/', accounts.views.signupsuccessful, name='signupsuccessful'),  #For TEST purposes only! To be deleted after main page implementation.


]
