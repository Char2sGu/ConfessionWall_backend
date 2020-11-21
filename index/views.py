from typing import Iterable

from django.db.models import Count
from django.db.utils import IntegrityError
from django.http.request import QueryDict
from django.contrib import auth

from rest_framework.exceptions import ParseError, AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from . import models, serializers


def extract_items(d: dict, keys: Iterable, safe=True):
    """Extract keys from a dict.

    Args:
        safe: When set to False, it may extract keys that do not exists and cause KeyError.
    """
    return {k: d[k] for k in keys if not safe or k in d}


class ConfessionAPIViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin, ListModelMixin, DestroyModelMixin):
    serializer_class = serializers.ConfessionSerializer
    queryset = models.Confession.objects.all()

    def get_queryset(self):
        try:
            query_params: QueryDict = self.request.query_params
            sort = {'latest': ('-id',),
                    'earlest': ('id',),
                    'hottest': ('-likes', '-comments'),
                    'coldest': ('likes', 'comments'),
                    }[query_params.get('sort', 'latest')]
            person = query_params.get('person')
            queryset = models.Confession.objects.annotate(
                likes=Count('like', distinct=True),
                comments=Count('comment', distinct=True)
            ).order_by(*sort)
            if person:
                queryset = queryset.filter(
                    sender=person) | queryset.filter(receiver=person)
        except (KeyError, ValueError) as e:
            raise ParseError(e)
        return queryset

    def get_permissions(self):
        return {
            'destory': [IsAdminUser()]
        }.get(self.action, super().get_permissions())


class PersonAPIViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin, ListModelMixin):
    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.all()

    def get_queryset(self):
        try:
            queryset = models.Person.objects.all()
            query_params: QueryDict = self.request.query_params
            contains = query_params.get('contains')
            if contains:
                assert len(contains) >= 2, 'Expected at least 2 letters.'
                queryset = queryset.filter(display_name__contains=contains)
            return queryset
        except AssertionError as e:
            raise ParseError(e)

    def create(self, request: Request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            data = extract_items(request.data, ['display_name', 'sex'])
            instance = models.Person.objects.get(**data)
            data = self.get_serializer(instance=instance).data
            return Response(data)


class LikeAPIViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = serializers.LikeSerializer
    queryset = models.Like.objects.all()


class CommentAPIViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def get_queryset(self):
        if self.action == 'list':
            try:
                confession = self.request.query_params['confession']
            except KeyError as e:
                raise ParseError(e)
            queryset = models.Comment.objects.all()
            queryset = queryset.filter(confession=confession)
            return queryset
        else:
            return super().get_queryset()

    def get_permissions(self):
        return {
            'destory': [IsAdminUser()]
        }.get(self.action, super().get_permissions())


class AuthAPIView(APIView):
    def post(self, request: Request):
        action = request.data.get('action', 'logout')
        if action == 'login':
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
        elif action == 'logout':
            auth.logout(request)
            return Response(str(request.user))
        else:
            raise ParseError()
