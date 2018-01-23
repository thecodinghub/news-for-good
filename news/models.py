from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse
import misaka
# Create your models here.

User = get_user_model()

VOTE_TYPE = (("U", "Up"),("D", "Down"))

class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts')
    created_at = models.DateTimeField(auto_now=True)
    heading = models.CharField(max_length=150,blank=False)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    image = models.ImageField(upload_to = 'news/')
    total_votes = models.IntegerField(editable=False, default = 0)
    up_votes = models.IntegerField(editable=False, default = 0)
    down_votes = models.IntegerField(editable=False, default = 0)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('news:single',kwargs={'username':self.user.username,
        'pk':self.pk})

    def upvote(self, user):
        uservote, created = UserVotes.objects.get_or_create(user = user, post = self)
        uservote.vote_type = "U"
        uservote.save()
        self.up_votes = self.post_votes.filter(vote_type = "U").count()
        if created:
            # Should have 1 more total vote than before was created
            self.total_votes = self.post_votes.all().count()
        else:
            # Should be 1 fewer upvotes than before, to account for swapping to U
            # But same total_votes, no need to recount.
            self.down_votes = self.post_votes.filter(vote_type = "D").count()
        self.save()

    def downvote(self, user):
        uservote, created = UserVotes.objects.get_or_create(user = user, post = self)
        uservote.vote_type = "D"
        uservote.save()
        self.down_votes = self.post_votes.filter(vote_type = "D").count()
        if created:
            # Should have 1 more total vote than before was created
            self.total_votes = self.post_votes.all().count()
        else:
            # Should be 1 fewer upvotes than before, to account for swapping to D
            # But same total_votes, no need to recount.
            self.up_votes = self.post_votes.filter(vote_type = "U").count()
        self.save()

    def user_vote(self, user):
        try:
            return UserVotes.objects.get(user = user, post = self)
        except UserVotes.DoesNotExist:
            return None

    class Meta():
        ordering = ['-created_at']

class UserVotes(models.Model):
    user = models.ForeignKey(User, related_name="user_votes")
    post = models.ForeignKey(Post, related_name="post_votes")
    vote_type = models.CharField(blank=False, max_length=100, choices = VOTE_TYPE, default = VOTE_TYPE[0][0])

    class Meta:
        unique_together = ('user', 'post')

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
