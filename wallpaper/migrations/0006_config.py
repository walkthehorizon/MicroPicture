# Generated by Django 2.2.1 on 2020-09-14 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallpaper', '0005_auto_20200817_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newest_version', models.IntegerField(default=100, help_text='当前App最新的版本号', verbose_name='版本号')),
            ],
        ),
    ]
