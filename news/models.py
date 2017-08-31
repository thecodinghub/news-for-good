from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse
import misaka
# Create your models here.

User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    total_votes = models.IntegerField(editable=False,default = 0)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('news:single',kwargs={'username':self.user.username,
        'pk':self.pk})

    def upvote(self):
        self.total_votes = self.total_votes+1
        self.save()

    def downvote(self):
        self.total_votes = self.total_votes-1
        self.save()

    class Meta():
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey('news.Post',related_name='comments')
    aurthor = models.CharField(blank=False, max_length=100)
    comment = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now = True)
    comment_html = models.TextField(editable = False)

    def save(self,*args,**kwargs):
        self.comment_html = misaka.html(self.comment)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        #print(self.pk,self.post_id,self.post_user)
        return reverse('news:all')

    def __str__(self):
        return self.comment
