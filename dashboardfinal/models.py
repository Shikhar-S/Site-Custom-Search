from django.db import models

# Create your models here.
class Crawler(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    domain=models.CharField(max_length=100)

class ResultPageX(models.Model):
    websitename=models.CharField(max_length=50)
    tagline = models.CharField(max_length=50)
    companyLogo = models.ImageField(upload_to='./static/pic_folder/', default='img/sample.jpeg')
    headerTemplate=models.CharField(max_length=50)
    numberOfResults=models.IntegerField(default=5)
    bodyTemplate=models.CharField(max_length=50)
    crawler = models.ForeignKey(Crawler, related_name="resultpagex", on_delete=models.CASCADE)

class Metrics(models.Model):
    #crawler_ref=models.ForeignKey(Crawler, on_delete=models.CASCADE)
    crawlerName=models.CharField(max_length=100)
    userQuery=models.CharField(max_length=300)
    queryCount=models.IntegerField(default=0)

