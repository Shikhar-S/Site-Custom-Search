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
    companyLogo = models.ImageField(upload_to='./static/pic_folder/', default='img/sample.jpeg')
    crawler=models.ForeignKey(Crawler,related_name="resultpage",on_delete=models.CASCADE)



class ResultPageX(models.Model):
    tagline = models.CharField(max_length=50)
    adDisplayLeftCount = models.IntegerField(default=0)
    adDisplayRightCount = models.IntegerField(default=0)
    adDisplayCenterTopCount = models.IntegerField(default=0)
    adDisplayCenterBottomCount = models.IntegerField(default=0)
    companyLogo = models.ImageField(upload_to='./static/pic_folder/', default='img/sample.jpeg')
    crawler = models.ForeignKey(Crawler, related_name="resultpagex", on_delete=models.CASCADE)

class Image(models.Model):
    image=models.ImageField(upload_to = './static/pic_folder/',default='img/sample.jpeg')

