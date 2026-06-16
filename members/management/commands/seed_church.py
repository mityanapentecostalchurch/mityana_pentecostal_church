from django.core.management.base import BaseCommand
from members.models import Department, Role


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        departments = [
            "Pastoral Ministry",
            "Administration",
            "Finance",
            "Youth Ministry",
            "Music / Choir Ministry",
            "Women's Ministry",
            "Men's Ministry",
            "Children's Ministry",
            "Media Ministry",
            "Evangelism Ministry",
            "Hospitality Ministry",
            "Ushering Ministry",
            "Prayer Ministry",
            "Elders Council",
            "Deacons Ministry",
            "Development Committee",
        ]

        roles = [
            "Lead Apostle",
            "Lead Pastor",
            "Associate Pastor",
            "Assistant Pastor",
            "Secretary",
            "Treasurer",
            "Youth Leader",
            "Choir Leader",
            "Women's Leader",
            "Men's Leader",
            "Children's Ministry Leader",
            "Media Leader",
            "Evangelism Leader",
            "Hospitality Leader",
            "Chief Usher",
            "Intercessory Leader",
            "Elder",
            "Deacon",
            "Chairperson",
            "Department Member",
        ]

        for name in departments:
            Department.objects.get_or_create(
                name=name
            )

        for name in roles:
            Role.objects.get_or_create(
                name=name
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Church structure created successfully."
            )
        )