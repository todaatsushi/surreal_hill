# Generated by Django 2.1.7 on 2019-03-21 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='header',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
