from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from django.views import generic
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()

from . import models
from . import forms
# Create your views here.

class PostList(generic.ListView):
    model = models.Post

class UserPost(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
                )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class Postdetail(generic.DetailView):
    model=models.Post

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact = self.kwargs.get(
        'username'
        ))

class CreatePost(LoginRequiredMixin,generic.CreateView):

    fields = ('message',)
    model = models.Post

    login_url = "/users/login"

    def form_valid(self,form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeleteView(LoginRequiredMixin,generic.DeleteView):
    model = models.Post
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delte(self,*args,**kwargs):
        message.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)


class CommentCreateView(LoginRequiredMixin,generic.CreateView):
    model = models.Comment
    fields = ('comment',)

    login_url = "/users/login"

    def form_valid(self,form,*args,**kwargs):

        self.object = form.save(commit = False)
        self.object.aurthor = self.request.user.username
        self.object.post_id = self.kwargs['pk']
        self.object.save()
        return super().form_valid(form)

@login_required
def upvote(request,pk):
    login_url = 'users/login'
    post = get_object_or_404(models.Post,pk=pk)
    user = request.user
    post.upvote(user)
    return redirect('posts:single',username=post.user,pk=pk)

@login_required
def downvote(request,pk):
    post = get_object_or_404(models.Post,pk=pk)
    user = request.user
    post.downvote(user)
    return redirect('posts:single',username=post.user,pk=pk)
