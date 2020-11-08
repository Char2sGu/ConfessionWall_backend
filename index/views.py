from django.db.models import QuerySet, Count
from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from . import models, serializers


class ConfessionAPIView(APIView):
    def get(self, request: Request):
        """Get a confession.
        """
        try:
            confession = request.query_params['id']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        confession = models.Confession.objects.get(id=confession)
        serializer = serializers.ConfessionSerializer(instance=confession)
        return Response(serializer.data)

    def post(self, request: Request):
        """Create a confession.
        """
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


class ConfessionPageAPIView(APIView):
    def get(self, request: Request):
        """Get a page of confessions.
        """
        page = int(request.query_params.get('page', 1))
        sort = request.query_params.get('sort', 'latest')
        try: # convert into params
            sort = {'latest': ('-id',), 'earlest': ('id',),
                    'hottest': ('-likes', '-comments',), 'coldest': ('likes', 'comments',)}[sort]
        except KeyError: # unsupported sort
            return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset: QuerySet = models.Confession.objects.all()
        queryset = queryset.annotate(
            likes=Count('like', distinct=True),
            comments=Count('comment', distinct=True)
        ).order_by(*sort)

        paginator = Paginator(queryset, 10)
        data = paginator.get_page(page)

        serializer = serializers.ConfessionSerializer(data, many=True)
        return Response({
            'data': serializer.data,
            'total_pages': paginator.num_pages,
        })



class LikeAPIView(APIView):
    def post(self, request: Request):
        """Create a like.
        """
        try:
            confession_id = request.data['confession']
            confession = models.Confession.objects.get(id=confession_id)
            models.Like.objects.create(confession=confession)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentAPIView(APIView):
    def post(self, request: Request):
        """Create a comment.
        """
        try:
            confession_id = request.data['confession']
            confession = models.Confession.objects.get(id=confession_id)
            serializer = serializers.CommentSerializer(data=request.data)
            assert serializer.is_valid()
            serializer.save(confession=confession)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentPageAPIView(APIView):
    def get(self, request: Request):
        """Get a page of comments.
        """
        try:
            confession_id = request.query_params['confession']
            requested_page = int(request.query_params.get('page', 1))

            confession = models.Confession.objects.get(id=confession_id)
            data = confession.comment_set.order_by('-id')
            paginator = Paginator(data, 5)
            data = paginator.get_page(requested_page)

            serializer = serializers.CommentSerializer(data, many=True)
            return Response({
                "data": serializer.data,
                "total_pages": paginator.num_pages,
            })
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

