from django.core.management.base import BaseCommand, CommandError
from my_app.models import Tag, CustomUser

class Command(BaseCommand):
    help = 'Fill the database'

    def handle(self, *args, **options):
        user = CustomUser.objects.get(email = 'rudnev.vanya@gmail.com')
	Tag.objects.all().delete()
	for i in range (100):
		t = Tag(
			text = 'tag ' + str(i),
		)
		t.save()
