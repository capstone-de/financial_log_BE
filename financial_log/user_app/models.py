from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=10)
    password = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'User'

    def __str__(self):
        return self.nickname


class Follow(models.Model):
    follow_id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    status = models.IntegerField(db_comment='1 == 수락\n0 == 대기')

    class Meta:
        managed = False
        db_table = 'Follow'
