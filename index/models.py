from django.db import models


class Person(models.Model):
    nickname = models.CharField(max_length=30, primary_key=True)
    realname = models.CharField(max_length=10)
    sex = models.CharField(max_length=1, choices=[
        ('m', 'Male'), ('f', 'Female'), ('', 'Unknow')
    ])
    creation_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[ {self.sex} - {self.nickname} @ {self.creation_time} ]"


class Confession(models.Model):
    sender = models.ForeignKey(Person, models.CASCADE, 'sender_id')
    receiver = models.ForeignKey(Person, models.CASCADE, 'receiver_id')
    creation_time = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=2000)

    def __str__(self):
        likes = self.like_set.count()
        comments = self.comment_set.count()
        return f"[ {self.sender.nickname} to {self.receiver.nickname} with {likes} likes and {comments} comments @ {self.creation_time} ]"


class Comment(models.Model):
    confession = models.ForeignKey(Confession, models.CASCADE)
    text = models.TextField(max_length=50)
    creation_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[ {self.text[:10]} to {self.confession} @ {self.creation_time} ]"


class Like(models.Model):
    confession = models.ForeignKey(Confession, models.CASCADE)
    creation_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[ To {self.confession} @ {self.creation_time} ]"
