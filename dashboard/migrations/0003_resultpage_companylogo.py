# Generated by Django 2.1 on 2018-08-22 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultpage',
            name='companyLogo',
            field=models.ImageField(default='./static/img/sample.jpeg', upload_to='./static/pic_folder/'),
        ),
    ]