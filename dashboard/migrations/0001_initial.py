# Generated by Django 2.1 on 2018-08-26 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crawler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('domain', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='img/sample.jpeg', upload_to='./static/pic_folder/')),
            ],
        ),
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crawler_name', models.CharField(max_length=100)),
                ('userQuery', models.CharField(max_length=300)),
                ('queryCount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ResultPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adDisplayLeft', models.BooleanField()),
                ('adDisplayLeftCount', models.IntegerField(default=0)),
                ('adDisplayRight', models.BooleanField()),
                ('adDisplayRightCount', models.IntegerField(default=0)),
                ('companyLogo', models.ImageField(default='img/sample.jpeg', upload_to='./static/pic_folder/')),
                ('crawler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultpage', to='dashboard.Crawler')),
            ],
        ),
        migrations.CreateModel(
            name='ResultPageX',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagline', models.CharField(max_length=50)),
                ('adDisplayLeftCount', models.IntegerField(default=0)),
                ('adDisplayRightCount', models.IntegerField(default=0)),
                ('adDisplayCenterTopCount', models.IntegerField(default=0)),
                ('adDisplayCenterBottomCount', models.IntegerField(default=0)),
                ('companyLogo', models.ImageField(default='img/sample.jpeg', upload_to='./static/pic_folder/')),
                ('crawler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultpagex', to='dashboard.Crawler')),
            ],
        ),
    ]
