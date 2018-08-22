from django import forms
from .models import Crawler
from .models import Image


class NewCrawlerForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    description=forms.CharField(max_length=100)
    domain=forms.CharField(max_length=100)


    adDisplayLeft = forms.BooleanField(required=False)
    adDisplayLeftCount = forms.IntegerField(required=False)
    adDisplayRight = forms.BooleanField()
    adDisplayRightCount = forms.IntegerField()
    companyLogo=forms.ImageField()


    class Meta:
        model = Crawler
        fields = ['name', 'description','domain']+\
                  ['adDisplayLeft','adDisplayRight','adDisplayLeftCount','adDisplayRightCount','companyLogo']


class NewImageUploadForm(forms.ModelForm):
    image=forms.ImageField()

    class Meta:
        model=Image
        fields=['image']