# Generated by Django 2.1.7 on 2019-05-30 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallpaper', '0036_auto_20190530_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
