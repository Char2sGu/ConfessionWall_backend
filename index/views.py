from django.db.models import QuerySet
from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from . import models, serializers


class ConfessionAPIView(APIView):
    def get(self, request: Request):
        queryset: QuerySet = models.Confession.objects.all()
        queryset = queryset.order_by('-id')

        paginator = Paginator(queryset, 10)
        requested_pagenum = int(request.query_params.get('page', 1))
        data = paginator.get_page(requested_pagenum)

        serializer = serializers.ConfessionSerializer(data, many=True)
        return Response({
            'data': serializer.data,
            'total_pages': paginator.num_pages,
        })

    def post(self, request: Request):
        serializer = serializers.ConfessionSerializer(data=request.data)
        if serializer.is_valid() and 'sender' in request.data and 'receiver' in request.data:
            sender = self.get_person(request.data['sender'])
            receiver = self.get_person(request.data['receiver'])
            serializer.save(sender=sender, receiver=receiver)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_person(self, data):
        try:
            person: models.Person = models.Person.objects.get(nickname=data['nickname'])
            if person.realname != data['realname']:
                person.realname = data['realname']
                person.save()
        except:
            person = models.Person.objects.create(**data)
        return person


class LikeAPIView(APIView):
    def post(self, request: Request):
        try:
            confession_id = request.data['id']
            confession = models.Confession.objects.get(id=confession_id)
            models.Like.objects.create(confession=confession)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
