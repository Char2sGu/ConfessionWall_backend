from django.db.models import QuerySet, Count
from django.contrib import auth

from rest_framework.exceptions import ParseError, NotFound, AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from . import models, serializers


class ConfessionAPIViewSet(RetrieveModelMixin, CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = serializers.ConfessionSerializer
    queryset = models.Confession.objects.all()

    def get_queryset(self):
        try:
            sort = self.request.query_params.get('sort', 'latest')
            sort = {'latest': ('-id',), 'earlest': ('id',),
                    'hottest': ('-likes', '-comments',), 'coldest': ('likes', 'comments',)}[sort]
        except:
            raise ParseError()

        return models.Confession.objects.annotate(
            likes=Count('like', distinct=True),
            comments=Count('comment', distinct=True)
        ).order_by(*sort)

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser()]
        else:
            return super().get_permissions()


class PersonAPIViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.all()

    @action(detail=False)
    def id(self, request: Request):
        try:
            query_params = dict(request.query_params.items())
            query_params = {
                'display_name':  query_params['display_name'],
                'sex': query_params['sex']
            }
            obj = models.Person.objects.get(**query_params)
        except KeyError as e:
            raise ParseError(e)
        except models.Person.DoesNotExist as e:
            raise NotFound(e)
        return Response(obj.pk)


class LikeAPIViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = serializers.LikeSerializer
    queryset = models.Like.objects.all()


class CommentAPIViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def get_queryset(self):
        if self.action == 'list':
            try:
                confession = self.request.query_params['confession']
            except KeyError as e:
                raise ParseError(e)
            queryset: QuerySet = models.Comment.objects.all()
            queryset = queryset.filter(confession=confession)
            return queryset
        else:
            return super().get_queryset()

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser()]
        else:
            return super().get_permissions()


class AuthAPIView(APIView):
    def post(self, request: Request):
        if request.data['action'] == 'login':
            try:
                username: str = request.data['username']
                password: str = request.data['password']
            except KeyError as e:
                raise ParseError(e)
            if user := auth.authenticate(username=username, password=password):
                auth.login(request, user)
                return Response(str(user))
            else:
                raise AuthenticationFailed()
        elif request.data['action'] == 'logout':
            auth.logout(request)
            return Response(str(request.user))
        else:
            raise ParseError()
