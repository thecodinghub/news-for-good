from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


app_name = 'users'

urlpatterns = [
    url(r'^signup/$',views.UserCreateForm.as_view(), name='signup'),
    url(r'login/$',auth_views.LoginView.as_view(template_name="users/login.html"),name='login'),
]
