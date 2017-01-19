from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime

class QuestionManager(models.Manager):
	def new(self):
		return self.order_by('-added_at')
	def top(self):
		return self.order_by('-rating')
	def tag(self, tag_id):
		return self.filter(tags__id__exact = tag_id).order_by('-added_at')



class Question(models.Model):
	title = models.CharField (max_length = 128)
	text = models.TextField()
	added_at = models.DateTimeField(default = datetime.datetime.now)
	author = models.ForeignKey('Profile')
	rating = models.IntegerField(default = 0)
	votes = models.ManyToManyField('Profile', related_name='voted_users', through='Like')
	tags = models.ManyToManyField('Tag')
	answers_num = models.IntegerField(default=0)
	objects = QuestionManager()
	correct_answer = models.IntegerField(default = -1)
	
	
class Answer (models.Model):
	text = models.TextField()
	author = models.ForeignKey('Profile')
	question = models.ForeignKey(Question)	
	added_at = models.DateTimeField(default = datetime.datetime.now)
	rating = models.IntegerField(default=0)
	is_correct = models.BooleanField(default=False)

class Like (models.Model):
	user = models.ForeignKey('Profile')
	question = models.ForeignKey(Question)
	is_like = models.BooleanField(default=True)
	class Meta:
		unique_together = ("user", "question")



class TagManager(models.Manager):
	def top(self):
		return self.order_by('-num_questions')[:10]

class Tag(models.Model):
	text = models.CharField (max_length = 30, unique=True)
	num_questions = models.IntegerField(default=0)
	objects = TagManager()


class ProfileManager(models.Manager):
	def top(self):
		return self.order_by('-rating')[:5]

class Profile(models.Model):
	user = models.OneToOneField(User)
	avatar = models.ImageField(upload_to='uploads/')
	rating = models.IntegerField(default=0)
	objects = ProfileManager()
	
	
	
