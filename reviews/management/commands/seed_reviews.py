import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from rooms.models import Room
from users.models import User


class Command(BaseCommand):

    help = "This command creates reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many reviews do you want to create",
        )
        pass

    def handle(self, *args, **options):
        number = options.get("number")
        users = User.objects.all()
        rooms = Room.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            Review,
            number,
            {
                "accuracy": lambda x: random.randint(0, 5),
                "communication": lambda x: random.randint(0, 5),
                "cleanliness": lambda x: random.randint(0, 5),
                "location": lambda x: random.randint(0, 5),
                "check_in": lambda x: random.randint(0, 5),
                "value": lambda x: random.randint(0, 5),
                "user": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created!"))
