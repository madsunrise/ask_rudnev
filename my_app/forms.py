#-*-coding: utf-8-*-.
from django import forms
from my_app.models import Question, Profile
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input inputlogin'}), label=u'Имя пользователя', max_length = 30)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input inputlogin'}), label=u'Пароль', max_length = 30)
	redirect = forms.CharField(widget=forms.HiddenInput, label='')

class SignupForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input inputlogin'}), label=u'Логин', max_length = 30)
	email    = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'input inputlogin'}), label='E-mail', max_length = 30)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input inputlogin'}), label=u'Пароль', max_length = 30)
	repeat_password = forms.CharField(widget = forms.PasswordInput(attrs={'class' : 'input inputlogin'}), label=u'Повторите пароль', max_length = 30)
	redirect = forms.CharField(widget=forms.HiddenInput, label='')
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username=username).exists():
			self._errors["username"] = self.error_class([u'Пользователь с таким именем уже существует'])
			del self.cleaned_data["username"]
		return username

	def clean(self):
		cleaned_data = super(SignupForm, self).clean()
		password = self.cleaned_data.get('password','')
		repeat_password = self.cleaned_data.get('repeat_password','')
		if password != repeat_password:
			self._errors["password"] = self.error_class([u'Пароли не совпадают'])
		elif len(password) < 6:
			self._errors["password"] = self.error_class([u'Введите пароль длиной не менее 6 символов'])
		return cleaned_data


class AvatarForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = (
			'avatar',
		)




    


class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'text']
		widgets = {
			'title' : forms.TextInput(attrs={'class' : 'input'}),
			'text' : forms.Textarea(attrs={'class' : 'input'})
		}
		labels = {
			'title': u'Название',
			'text': u'Текст вопроса'
		}

	tags = forms.CharField (widget = forms.TextInput(attrs={'class' : 'input'}), label=u'Теги (через запятую)', required=False)

	def __init__(self, *args, **kwargs):
		self.author = kwargs.pop('author', None)
		super(QuestionForm, self).__init__(*args,  **kwargs)

	def save(self, commit=True):
		obj = super(QuestionForm, self).save(commit=False)
		obj.author = self.author
		if commit:
			obj.save()
		return obj




class AnswerForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea(attrs={'class' : 'input'}))

	def save(self, q_id, user):
		question = Question.objects.get(pk=q_id)
		author = Profile.objects.get(user=user)
		question.answers_num += 1
		question.save()
		return question.answer_set.create(text=self.cleaned_data['text'], author=author)



class UpdateProfileForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input inputlogin'}), label=u'Логин', max_length = 30)
	email    = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'input inputlogin'}),label=u'Email', max_length = 30)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input inputlogin'}), label=u'Новый пароль', max_length = 30, required=False)
	repeat_password = forms.CharField(widget = forms.PasswordInput(attrs={'class' : 'input inputlogin'}),label=u'Повторите пароль',  max_length = 30, required=False)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if username != self.instance.username and User.objects.filter(username=username).exists():
			self._errors["username"] = self.error_class([u'Пользователь с таким именем уже существует'])
			del self.cleaned_data["username"]
		return username


	def clean_repeat_password(self):
		password = self.cleaned_data.get('password', '')
		repeat_password = self.cleaned_data.get('repeat_password', '')
		if password != repeat_password:
			raise forms.ValidationError(u'Пароли не совпадают')

		if password != '' and len(password) < 6:
			raise forms.ValidationError(u'Введите пароль длиной не менее 6 символов')


	def __init__(self, *args, **kwargs):
		super(UpdateProfileForm, self).__init__(*args, **kwargs)
		self.fields['username'].initial = self.instance.username
		self.fields['email'].initial = self.instance.email

	def save(self, *args, **kwargs):
		super(UpdateProfileForm, self).save(*args, **kwargs)
		self.instance.username = self.cleaned_data.get('username')
		self.instance.email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password', '')
		if (password != ''):
			self.instance.set_password(password)
		self.instance.save()

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class AvatarEditForm(forms.Form):
	avatar = forms.ImageField (required=False)
