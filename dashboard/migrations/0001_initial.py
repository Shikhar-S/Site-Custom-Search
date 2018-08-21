# Generated by Django 2.1 on 2018-08-21 08:27

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
            name='ResultPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adDisplayLeft', models.BooleanField()),
                ('adDisplayLeftCount', models.IntegerField(default=0)),
                ('adDisplayRight', models.BooleanField()),
                ('adDisplayRightCount', models.IntegerField(default=0)),
                ('crawler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultpage', to='dashboard.Crawler')),
            ],
        ),
    ]