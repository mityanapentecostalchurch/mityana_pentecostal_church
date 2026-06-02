from rest_framework import generics

from members.models import Member, Department
from events.models import Event
from announcements.models import Announcement
from sermons.models import Sermon
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    MemberSerializer,
    DepartmentSerializer, EventSerializer, AnnouncementSerializer, SermonSerializer,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User


class MemberListAPIView(
    generics.ListAPIView
):

    queryset = Member.objects.all()

    serializer_class = MemberSerializer


class DepartmentListAPIView(
    generics.ListAPIView
):

    queryset = Department.objects.all()

    serializer_class = DepartmentSerializer



class EventListAPIView(
    generics.ListAPIView
):

    queryset = Event.objects.all()

    serializer_class = EventSerializer

class AnnouncementListAPIView(
    generics.ListAPIView
):

    queryset = Announcement.objects.all()

    serializer_class = AnnouncementSerializer

class SermonListAPIView(
    generics.ListAPIView
):

    queryset = Sermon.objects.all()

    serializer_class = SermonSerializer

class MemberListAPIView(
    generics.ListAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = Member.objects.all()

    serializer_class = MemberSerializer

class CurrentUserAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'role': request.user.role,
        })