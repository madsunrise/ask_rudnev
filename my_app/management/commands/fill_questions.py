from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from my_app.models import Question, Tag, Profile
from faker import Factory
import random

class Command(BaseCommand):
    def handle(self, *args, **options):

	Question.objects.all().delete()
	Tag.objects.all().delete()
	fake = Factory.create('ru_RU')
	for i in range (100000):
		u = User.objects.get(pk = random.randint(100, 1000))
		user = Profile.objects.get(user=u)
		user.rating += 1;
		user.save()
		q = Question(
			author=user,
			text = fake.text(),
			title = fake.name(),
		)
		q.save()
		if (random.randint(0, 1) == 1):
			for j in range (random.randint(0, 3)):
				rand = random.randint(0,10000)
				s = 'tag#{0}'.format(rand)
				if Tag.objects.filter(text=s).exists():
					t = Tag.objects.get(text=s)
				else:			
					t = Tag(text=s)
				t.num_questions += 1
				t.save()
				q.tags.add(t)
			q.save()
		
