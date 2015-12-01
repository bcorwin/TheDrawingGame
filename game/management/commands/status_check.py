from django.core.management.base import BaseCommand

from game.status_check import status_check

class Command(BaseCommand):
    args = None

    def handle(self, *args, **options):
        val = status_check()
        return(val)