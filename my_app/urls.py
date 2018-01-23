"""my_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from news import views as post_view

urlpatterns = [
    url(r'^$',post_view.PostList.as_view(), name='all'),
    url(r'^admin/', admin.site.urls),
    url(r'^users/',include('users.urls',namespace='users')),
    url(r'^users/',include('django.contrib.auth.urls')),
    url(r'^test/$',views.TestView.as_view(),name='test'),
    url(r'^thanks/$',views.ThanksView.as_view(),name='thanks'),
    url(r'^posts/', include('news.urls',namespace='news'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns  = [
        url('^__debug__/', include(debug_toolbar.urls)),
        # staticfiles_urlpatterns(),
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ] + urlpatterns

