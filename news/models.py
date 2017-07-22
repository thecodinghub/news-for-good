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

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('news:single',kwargs={'username':self.user.username,'pk':self.pk})

    class Meta():
        ordering = ['-created_at']
