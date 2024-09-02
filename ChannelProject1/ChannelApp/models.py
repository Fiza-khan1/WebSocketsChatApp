from django.db import models

class Group(models.Model):
    groupName=models.CharField(max_length=100)
    def __str__(self):
        return self.groupName


class Chat(models.Model):
    Gname=models.ForeignKey('Group',on_delete=models.CASCADE)
    content=models.CharField(max_length=200)
    timestamp=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content
