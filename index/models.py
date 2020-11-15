from django.db import models


class Person(models.Model):
    display_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1, choices=[
        ('M', 'Male'), ('F', 'Female'), ('X', 'Secret')
    ])
    creation_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('display_name', 'sex'), name='unique_person')
        ]

    def __str__(self):
        return f"{self.id:3} {self.display_name:15} {self.sex}"


class Confession(models.Model):
    sender = models.ForeignKey(Person, models.CASCADE, 'sender_id')
    receiver = models.ForeignKey(Person, models.CASCADE, 'receiver_id')
    creation_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=2000)

    def __str__(self):
        likes = self.like_set.count()
        comments = self.comment_set.count()
        return f"{self.id:4} {likes:4} {comments:3}"


class Comment(models.Model):
    confession = models.ForeignKey(Confession, on_delete=models.CASCADE)
    text = models.TextField(max_length=100)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id:5} [{self.identity}] -> [{self.confession}]"


class Like(models.Model):
    confession = models.ForeignKey(Confession, models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id:6} [{self.person}] -> [{self.confession}]"
