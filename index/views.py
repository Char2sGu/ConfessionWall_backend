from django.db.models import QuerySet, Count
from django.core.paginator import Paginator
from django.contrib.auth.models import User, AnonymousUser
from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from . import models, serializers


class ConfessionAPIView(APIView):
    def get(self, request: Request, confession: int = None):
        """Get a confession.
        """
        if not confession:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            confession = models.Confession.objects.annotate(
                likes=Count('like', distinct=True),
                comments=Count('comment', distinct=True)
            ).get(id=confession)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ConfessionSerializer(instance=confession)
        return Response(serializer.data)

    def post(self, request: Request, confession: int = None):
        """Create a confession.
        """
        if confession:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = serializers.ConfessionSerializer(data=request.data)
        if serializer.is_valid() and 'sender' in request.data and 'receiver' in request.data:
            sender = self.get_person(request.data['sender'])
            receiver = self.get_person(request.data['receiver'])
            serializer.save(sender=sender, receiver=receiver)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_person(self, data):
        """Get the `Person` object by using `data['nickname']` as
        its primary key if it exists, otherwise create it.
        This will update `Person.realname` if `data['realname']`
        is a different value.
        """
        try:
            person: models.Person = models.Person.objects.get(
                nickname=data['nickname'])
            if person.realname != data['realname']:
                person.realname = data['realname']
                person.save()
        except:
            person = models.Person.objects.create(**data)
        return person

    def delete(self, request: Request, confession: int = None):
        """Delete a confession.
        """
        if not confession:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if type(request.user) == AnonymousUser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            models.Confession.objects.get(id=confession).delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response()


class ConfessionPageAPIView(APIView):
    def get(self, request: Request, page: int):
        """Get a page of confessions.
        """
        sort = request.query_params.get('sort', 'latest')
        try:  # convert into params
            sort = {'latest': ('-id',), 'earlest': ('id',),
                    'hottest': ('-likes', '-comments',), 'coldest': ('likes', 'comments',)}[sort]
        except KeyError:  # unsupported sort
            return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset: QuerySet = models.Confession.objects.all()
        queryset = queryset.annotate(
            likes=Count('like', distinct=True),
            comments=Count('comment', distinct=True)
        ).order_by(*sort)

        paginator = Paginator(queryset, 5)
        data = paginator.get_page(page)

        serializer = serializers.ConfessionSerializer(data, many=True)
        return Response({
            'data': serializer.data,
            'total_pages': paginator.num_pages,
        })


class LikeAPIView(APIView):
    def post(self, request: Request, confession: int):
        """Create a like.
        """
        confession: models.Confession = models.Confession.objects.get(
            id=confession)
        models.Like.objects.create(confession=confession)
        return Response(status=status.HTTP_201_CREATED)


class CommentAPIView(APIView):
    def post(self, request: Request, confession: int, comment: int = None):
        """Create a comment.
        """
        if comment:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        confession: models.Confession = models.Confession.objects.get(
            id=confession)
        serializer = serializers.CommentSerializer(data=request.data)
        serializer.is_valid(True)
        serializer.save(confession=confession)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request, confession: int, comment: int = None):
        """Delete a comment.
        """
        if not comment:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if type(request.user) == AnonymousUser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            models.Comment.objects.get(id=comment).delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response()
        


class CommentPageAPIView(APIView):
    def get(self, request: Request, confession: int, page: int):
        """Get a page of comments.
        """
        confession: models.Confession = models.Confession.objects.get(
            id=confession)
        data = confession.comment_set.order_by('-id')
        paginator = Paginator(data, 5)
        data = paginator.get_page(page)
        serializer = serializers.CommentSerializer(data, many=True)
        return Response({
            "data": serializer.data,
            "total_pages": paginator.num_pages,
        })


class AuthAPIView(APIView):
    def post(self, request: Request):
        if request.data['action'] == 'login':
            try:
                username: str = request.data['username']
                password: str = request.data['password']
            except KeyError:
                return Response({'detail': 'missing params'}, status=status.HTTP_400_BAD_REQUEST)
            if user := auth.authenticate(username=username, password=password):
                auth.login(request, user)
                return Response()
            else:
                return Response({'detail': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.data['action'] == 'logout':
            auth.logout(request)
            return Response()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
