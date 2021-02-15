import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists.models import List
from rooms.models import Room
from users.models import User


class Command(BaseCommand):

    help = "This command creates lists"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many lists do you want to create",
        )
        pass

    def handle(self, *args, **options):
        number = options.get("number")
        users = User.objects.all()
        rooms = Room.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} lists created!"))
