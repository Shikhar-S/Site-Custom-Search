from django import forms
from .models import Crawler



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



class NewCrawlerFormX(forms.ModelForm):
    name = forms.CharField(max_length=30,required=True,label='name')
    description=forms.CharField(max_length=100,label='description')
    domain=forms.CharField(max_length=100,required=True,label='domain')

    tagline=forms.CharField(max_length=50,initial="Science behind adverd",required=True,label="Tagline")
    websiteName=forms.CharField(max_length=50,label="Website Name")
    headerTemplate=forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    numberOfResults=forms.IntegerField(max_value=15)

    companyLogo=forms.ImageField()


    class Meta:
        model = Crawler
        fields = ['name', 'description','domain']+ \
                 ['tagline','websiteName','headerTemplate', 'companyLogo']