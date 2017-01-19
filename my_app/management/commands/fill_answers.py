#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from my_app.models import Question, Answer, Profile
import random
from faker import Factory

class Command(BaseCommand):
    help = 'Fill the answers'

    def handle(self, *args, **options):
	u = User.objects.get(pk=random.randint(1000, 2000))
	user = Profile.objects.get(user=u)
	Answer.objects.all().delete()
	questions = Question.objects.filter(pk__gt=202556)
	fake = Factory.create('ru_RU')
	for qs in questions:
		qs.answers_num = 0
		for i in range(0, random.randint(0,20)):
			a = Answer(
				text=u'Ответ #{0}    '.format(i) + fake.text(),
				author=user,
				question=qs,
			)
			a.save()
			qs.answers_num += 1
			qs.save()







