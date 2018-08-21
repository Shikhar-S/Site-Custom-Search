from django.db import models

# Create your models here.
class Crawler(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    domain=models.CharField(max_length=100)


class ResultPage(models.Model):

    adDisplayLeft=models.BooleanField()
    adDisplayLeftCount=models.IntegerField(default=0)
    adDisplayRight=models.BooleanField()
    adDisplayRightCount=models.IntegerField(default=0)

    crawler=models.ForeignKey(Crawler,related_name="resultpage",on_delete=models.CASCADE)


