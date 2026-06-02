# api/serializers.py

from rest_framework import serializers
from members.models import Member
from members.models import Department
from events.models import Event
from announcements.models import Announcement
from sermons.models import Sermon
from attendance.models import Attendance
from attendance.models import Service
from giving.models import Contribution



class MemberSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Member

        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class EventSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Event
        fields = '__all__'

class AnnouncementSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Announcement
        fields = '__all__'

class SermonSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Sermon
        fields = '__all__'

class AttendanceSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Attendance
        fields = '__all__'

class ServiceSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Service
        fields = '__all__'

class ContributionSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Contribution
        fields = '__all__'