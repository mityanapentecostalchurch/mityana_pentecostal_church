# api/serializers.py

from rest_framework import serializers
from members.models import Member
from members.models import Department
from events.models import Event
from announcements.models import Announcement
from sermons.models import Sermon


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