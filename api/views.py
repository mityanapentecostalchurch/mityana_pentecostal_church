from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from activity.models import ActivityLog
# from activity.models import ActivityLog

from members.models import Member, Department
from events.models import Event
from announcements.models import Announcement
from sermons.models import Sermon
from attendance.models import Attendance, Service
from giving.models import Contribution
from django.db.models import Sum
from accounts.permissions import (
    IsTreasurer,
    IsSecretary
)

from .serializers import (
    MemberSerializer,
    DepartmentSerializer,
    EventSerializer,
    AnnouncementSerializer,
    SermonSerializer,
    AttendanceSerializer,
    ServiceSerializer,
    ContributionSerializer, ActivityLogSerializer,
)


class MemberListAPIView(
    generics.ListAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = Member.objects.all()

    serializer_class = MemberSerializer

class MemberDetailAPIView(
    generics.RetrieveAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = Member.objects.all()

    serializer_class = MemberSerializer

class DepartmentListAPIView(
    generics.ListAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

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


class ServiceListAPIView(
    generics.ListAPIView
):

    queryset = Service.objects.all()

    serializer_class = ServiceSerializer


# class AttendanceListAPIView(
#     generics.ListAPIView
# ):

#     permission_classes = [
#         IsSecretary
#     ]

#     queryset = Attendance.objects.all()

#     serializer_class = AttendanceSerializer

class AttendanceAPIView(
    generics.ListCreateAPIView
):

    permission_classes = [
        IsSecretary
    ]

    def perform_create(self, serializer):

        attendance = serializer.save()

        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Recorded attendance for {attendance.member}"
        )

    queryset = Attendance.objects.all()

    serializer_class = AttendanceSerializer

    


# class ContributionListAPIView(
#     generics.ListAPIView
# ):

#     permission_classes = [
#         IsTreasurer
#     ]

#     queryset = Contribution.objects.all()

#     serializer_class = ContributionSerializer

class ContributionAPIView(
    generics.ListCreateAPIView
):

    permission_classes = [
        IsTreasurer
    ]
    def perform_create(self, serializer):

        contribution = serializer.save()

        ActivityLog.objects.create(
            user=self.request.user,
            action=(
                f"Recorded contribution "
                f"{contribution.amount}"
            )
        )

    queryset = Contribution.objects.all()

    serializer_class = ContributionSerializer

class CurrentUserAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'role': request.user.role,
        })

class ActivityLogAPIView(
    generics.ListAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = ActivityLog.objects.order_by(
        '-created_at'
    )

    serializer_class = ActivityLogSerializer

class DashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]
    

    def get(self, request):

        return Response({

            'members':
                Member.objects.count(),

            'departments':
                Department.objects.count(),

            'events':
                Event.objects.count(),

            'announcements':
                Announcement.objects.count(),

            'sermons':
                Sermon.objects.count(),

            'services':
                Service.objects.count(),

            'attendance':
                Attendance.objects.count(),

            'contributions':
                Contribution.objects.count(),
            'total_giving':
                Contribution.objects.aggregate(
                    total=Sum('amount')
                )['total'] or 0,
            

        })