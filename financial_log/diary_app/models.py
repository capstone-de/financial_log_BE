from django.db import models

from user_app.models import User

class Diary(models.Model):
    diary_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    contents = models.CharField(max_length=500)
    privacy = models.BooleanField(db_comment='1 == public\n0 == private\n')
    gu = models.ForeignKey(Gu)

    class Meta:
        managed = False
        db_table = 'Diary'


class Image(models.Model):
    image_id = models.IntegerField(primary_key=True)
    image = models.CharField(max_length=500)  # S3 URL을 저장
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Image'


class Hashtag(models.Model):
    hashtag_id = models.AutoField(primary_key=True)
    hashtag = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'Hashtag'


class DiaryHashtag(models.Model):
    table_id = models.AutoField(primary_key=True)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'DiaryHashtag'

class Gu(models.Model):
    gu_id = models.IntegerField(primary_key=True)
    gu = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'Gu'
    
