from django.conf.urls import url

from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^$',views.PostList.as_view(), name='all'),
    url(r'^new/$',views.CreatePost.as_view(), name='create'),
    url(r'^by/(?P<username>[-\w]+)$',views.UserPost.as_view(),name='for_user'),
    url(r'^by/(?P<username>[-\w]+)/(?P<pk>\d+)$',views.Postdetail.as_view(),name='single'),
    url(r'^delete/(?P<pk>\d+)',views.DeleteView.as_view(),name='delete'),
    url(r'^(?P<pk>\d+)/comment/',views.CommentCreateView.as_view(),name='add_comment'),
    url(r'^(?P<pk>\d+)/upvote/$', views.upvote, name='upvote'),
    url(r'^(?P<pk>\d+)/downvote/$', views.downvote, name='downvote'),
]
