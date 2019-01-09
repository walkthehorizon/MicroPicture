# Generated by Django 2.0.5 on 2019-01-09 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallpaper', '0029_auto_20190109_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='microuser',
            name='avatar',
            field=models.URLField(blank=True, default='\thttp://wallpager-1251812446.cosbj.myqcloud.com/avatar/default_avatar_7.823268836433075.jpg'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='cover',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='subject',
            name='cover_1',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='subject',
            name='cover_2',
            field=models.URLField(blank=True, default=''),
        ),
    ]
