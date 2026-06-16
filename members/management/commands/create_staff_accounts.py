from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):

    help = "Creates default church staff accounts"

    def handle(self, *args, **kwargs):

        accounts = [ ( "staff", "staff@mpc.org", "Staff123!" ), ( "visitor", "visitor@mpc.org", "Visitor123!" ), ]
        # accounts = [

        #     (
        #         "admin",
        #         "admin@mpc.org",
        #         "Admin123!"
        #     ),

        #     (
        #         "secretary",
        #         "secretary@mpc.org",
        #         "Secretary123!"
        #     ),

        #     (
        #         "treasurer",
        #         "treasurer@mpc.org",
        #         "Treasurer123!"
        #     ),

        #     (
        #         "youthleader",
        #         "youth@mpc.org",
        #         "Youth123!"
        #     ),

        #     (
        #         "choirleader",
        #         "choir@mpc.org",
        #         "Choir123!"
        #     ),

        # ]

        for username, email, password in accounts:

            if not User.objects.filter(
                username=username
            ).exists():

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created {username}"
                    )
                )

            else:

                self.stdout.write(
                    self.style.WARNING(
                        f"{username} already exists"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Staff accounts created."
            )
        )