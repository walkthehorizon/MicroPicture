import json

from django.contrib import auth
from django_filters import rest_framework
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from wallpaper import state
from wallpaper.permissions import IsOwnerOrReadOnly
from wallpaper.serializers import *
from wallpaper.state import CustomResponse, STATE_SUCCESS
from wallpaper.state import generate_result_json
from collections import OrderedDict


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'wallpapers': reverse('wallpaper-list', request=request, format=format)
    })


class CustomModelView(viewsets.ModelViewSet):
    # pagination_class = LargeResultsSetPagination
    # filter_class = ServerFilter
    # queryset = ''
    # serializer_class = ''
    # permission_classes = ()
    # filter_fields = ()
    # search_fields = ()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return CustomResponse(data=serializer.data,
                              headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(data=serializer.data, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse(data=serializer.data, )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return CustomResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse(data=[])


class CustomReadOnlyModelView(viewsets.ReadOnlyModelViewSet):
    queryset = ''
    serializer_class = ''
    permission_classes = ()
    filter_fields = ()
    search_fields = ()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse(data=serializer.data)


class UserList(generics.ListAPIView):
    queryset = MicroUser.objects.all()
    serializer_class = MicroUserSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)


@api_view(['POST'])
def register_user(request):
    print(request)
    print(request.data)
    phone = request.data.get('phone')
    password = request.data.get('password')
    if len(phone) != 11:
        return generate_result_json(state.STATE_PHONE_ERROR)
    if len(password) < 6:
        return generate_result_json(state.STATE_PASSWORD_ERROR)
    user = auth.authenticate(username=phone, password=password)
    if user is not None:
        return generate_result_json(state.STATE_USER_EXIST)
    user = MicroUser.objects.create_user(username=phone, phone=phone, password=password)
    user.save()
    return generate_result_json('注册成功', 1)


@api_view(['POST'])
def login_user(request):
    username = request.POST.get('phone', '')
    try:
        MicroUser.objects.get(username=username)
    except MicroUser.DoesNotExist:
        return generate_result_json(state.STATE_USER_NOT_EXIST)
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        data = json.dumps(MicroUserSerializer(user).data)
        print(data)
        print(type(data))
        return generate_result_json(1, data=data)
    else:
        # Show an error page
        return generate_result_json(state.STATE_PASSWORD_ERROR)


@api_view(['POST'])
def logout_user(request):
    print(request.user)
    auth.logout(request)
    return generate_result_json(1)


class WallPapersViewSet(CustomReadOnlyModelView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Wallpaper.objects.all()
    serializer_class = WallPaperSerializer
    filter_fields = ('subject_id',)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class WallPaperDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Wallpaper.objects.all()
    serializer_class = WallPaperSerializer


# 依照type筛选数据
class SubjectViewSet(CustomReadOnlyModelView):
    lookup_field = 'id'

    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return CustomResponse(serializer.data)

    # def filter_queryset(self, queryset):
    # limit = self.request.query_params.get('limit')
    # offset = self.request.query_params.get('offset')
    # if limit is None or offset is None:
    #     return queryset.filter(id=-1)
    # offset = int(offset)
    # limit = int(limit)
    # subject_type = self.request.query_params.get('subject_type')
    # if 0 < int(subject_type) < 4:
    #     queryset = queryset.filter(type=subject_type).order_by('-created')
    #     # for i in (offset, max(offset, min(offset + limit - 1, len(queryset) - 1))):
    #     #     subject = queryset[i]
    #     #     try:
    #     #         # print(subject.support_people.all())
    #     #         subject.support_people.all().get(id=self.request.user.id)
    #     #         subject.supported = True
    #     #     except MicroUser.DoesNotExist:
    #     #         subject.supported = False
    #     return queryset
    # else:
    #     queryset = queryset.order_by('-created')
    #     # for i in (offset, max(offset, min(offset + limit - 1, len(queryset) - 1))):
    #     #     subject = queryset[i]
    #     #     try:
    #     #         # print(subject.support_people.all())
    #     #         subject.support_people.all().get(id=self.request.user.id)
    #     #         subject.supported = True
    #     #     except MicroUser.DoesNotExist:
    #     #         subject.supported = False
    #     return queryset


class GetPictureByCategoryId(generics.ListAPIView):
    serializer_class = WallPaperSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # print(self.request.query_params.keys())
        return Wallpaper.objects.filter(category_id=self.kwargs.get('id'))


class GetSubjectWallpaper(generics.ListAPIView):
    serializer_class = WallPaperSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # print(self.request.query_params.keys())
        return Wallpaper.objects.filter(subject_id=self.kwargs.get('pk'))


# 获取所有分类
class CategoryList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


# 获取启动页数据
class GetSplash(generics.RetrieveAPIView):
    serializer_class = SplashSerializer
    queryset = Splash.objects.all().order_by('-id')

    def get_object(self):
        return self.queryset[0]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse(serializer.data)


class GetRandomRecommend(generics.ListAPIView):
    serializer_class = WallPaperSerializer
    queryset = Wallpaper.objects.all().order_by('?').distinct()

# @api_view(['PUT'])
# def put_subject_support(request):
#     user = request.user
#     if user is None or not user.is_active:
#         return generate_result_json(state_code=state.STATE_INVALID_USER)
#     subject_id = request.data.get('subjectId')
#     support_type = request.data.get('type')
#     subject = Subject.objects.get(id=subject_id)
#     if subject is None:
#         return generate_result_json(state_code=state.STATE_SUBJECT_NOT_EXIST)
#     if support_type == '1':
#         subject.support_people.add(user)
#     if support_type == '-1':
#         subject.support_people.remove(user)
#     # print(subject.support_people.all())
#     return generate_result_json(state_code=state.STATE_SUCCESS)
#
#
# @api_view(['GET'])
# def get_subject_support_count(request):
#     lookup_field = 'subjectId'
#     return generate_result_json(state_code=state.STATE_SUCCESS)
#     # subject_id = request.GET.get('subjectId', '2853')
#     # subject = Subject.objects.get(id=subject_id)
#     # if subject is None:
#     #     return generate_result_json(state_code=state.STATE_SUBJECT_NOT_EXIST)
#     # return generate_result_json(state_code=state.STATE_SUCCESS, data=str(len(subject.support_people.all())))
#
#
# class GetSubjectSupportCount(generics.GenericAPIView):
#     lookup_field = 'subjectId'
#
#     def get(self, request, subjectId):
#         try:
#             subject = Subject.objects.get(id=subjectId)
#         except Subject.DoesNotExist:
#             return Response(generate_result_json(state_code=state.STATE_SUBJECT_NOT_EXIST).content)
#         return Response(dump_result_json(state_code=state.STATE_SUCCESS, data=len(subject.support_people.all())))
