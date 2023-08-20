from django.db import models

from account.models import User
from utils.models import RichTextField


class Announcement(models.Model):
    title = models.TextField()
    # HTML
    content = RichTextField()
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update_time = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)
    top = models.BooleanField(default=False)

    class Meta:
        """
        -top:降序排序
        -create_time:降序排序
        """
        db_table = "announcement"
        ordering = ("-top","-create_time",)
