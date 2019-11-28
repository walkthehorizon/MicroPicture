from rest_framework import serializers
from wallpaper.models import *


class MicroUserSerializer(serializers.ModelSerializer):
    # "id": 1,
    # "last_login": "2018-07-03T09:17:28.915275Z",
    # "username": "shentu",
    # "email": "1308311472@qq.com",
    # "date_joined": "2018-07-02T10:05:53.214821Z",
    # "nickname": "神荼",
    # "phone": "18519118029",
    # "signature": "微梦官方编辑&程序&产品！",
    class Meta:
        model = MicroUser
        fields = ('id', 'nickname', 'avatar', 'phone', 'email', 'sex', 'signature', 'pea')


class WallPaperSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)

    class Meta:
        model = Wallpaper
        # owner = serializers.ReadOnlyField(source='owner.username')
        # subject = serializers.ReadOnlyField(source='subject.name')
        # owner = serializers.ReadOnlyField(source='owner.nickname')
        fields = ('id', 'url', 'origin_url', 'subject_id', 'collected', 'collect_num', 'created')


class SubjectSerializer(serializers.ModelSerializer):
    # wallpaper = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     queryset=Wallpaper.objects.all(),
    #     view_name="wallpaper-detail")

    # owner = MicroUserSerializer()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'cover', 'cover_1', 'cover_2', 'description', 'tag', 'created')
        # depth = 1


class CategorySerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'logo', 'description', 'created')


class SplashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Splash
        get_latest_by = 'id'
        fields = ('name', 'duration', 'cover_url', 'link_url')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'image_url', 'url', 'type', 'color', 'subject_id', 'title', 'desc')


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = '__all__'
