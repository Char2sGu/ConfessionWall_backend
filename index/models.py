from django.db import models


class Person(models.Model):
    # id
    nickname = models.CharField(max_length=30, primary_key=True)
    realname = models.CharField(max_length=10)
    sex = models.CharField(max_length=1, choices=[
        ('m', 'Male'), ('f', 'Female')
    ])
    creation_time = models.DateTimeField(auto_now=True)
    # like_set
    # confession_set

    def __str__(self):
        return f"[ {self.sex} - {self.nickname} @ {self.creation_time} ]"


class Confession(models.Model):
    # id
    sender = models.ForeignKey(Person, models.CASCADE, 'sender_id')
    receiver = models.ForeignKey(Person, models.CASCADE, 'receiver_id')
    creation_time = models.DateTimeField(auto_now=True)
    text = models.TextField()
    # like_set

    @property
    def like(self):
        return self.like_set.count

    def __str__(self):
        return f"[ {self.sender.nickname} to {self.receiver.nickname} with {self.like} likes @ {self.creation_time} ]"


class Like(models.Model):
    # id
    confession = models.ForeignKey(Confession, models.CASCADE)
    creation_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[ To {self.confession} @ {self.creation_time} ]"
