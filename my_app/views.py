#-*-coding: utf-8-*-.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from my_app.models import Question, Answer, Profile, Like, Tag
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from my_app.forms import SignupForm, LoginForm, QuestionForm, AvatarForm, AnswerForm, UpdateProfileForm,AvatarEditForm
import json




def paginate(parametr, request, num_of_list):
	contact_list = parametr
	paginator = Paginator(contact_list, num_of_list)
	page = request.GET.get('page')
	try:
		number_page = paginator.page(page)
	except PageNotAnInteger:
		number_page = paginator.page(1)
	except EmptyPage:
		number_page = paginator.page(paginator.num_pages)	
	return number_page



def top (request):
    questions = Question.objects.top()
    page = paginate(questions, request, 20)
    if (page.paginator.num_pages > 3):
        return render(request, 'index.html', { 'questions' : page, 'num_pages_minus2' :  page.paginator.num_pages - 2 } )
    else:
        return render(request, 'index.html', { 'questions' : page })





def index (request):
    questions = Question.objects.new()
    page = paginate(questions, request, 15)

    if (page.paginator.num_pages > 3):
        return render(request, 'index.html', { 'questions' : page, 'num_pages_minus2' :  page.paginator.num_pages - 2 } )
    else:
        return render(request, 'index.html', { 'questions' : page })




def question (request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.filter(question_id=question.id).order_by('-is_correct', 'added_at')
    if request.POST:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(question.id, request.user)
            return HttpResponseRedirect(request.path + '#' + (str)(answer.id))
        else:
            return render(request, 'question.html', {'question': question, 'answers': answers, 'form' : form })
    else:
        form = AnswerForm()
        return render(request, 'question.html', {'question' : question, 'answers' : answers, 'form': form })






def tag (request, tag_id):
    questions = Question.objects.tag(tag_id)
    page = paginate(questions, request, 15)
    tag = Tag.objects.get(pk=tag_id)
    if (page.paginator.num_pages > 3):
        return render(request, 'index.html', { 'questions' : page, 'num_pages_minus2' :  page.paginator.num_pages - 2, 'tag' : tag.text } )
    else:
        return render(request, 'index.html', { 'questions' : page, 'tag' : tag.text })



def ask (request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=' + request.path)
    if request.POST:
        p = Profile.objects.get(user=request.user)
        form = QuestionForm(request.POST, author=p)
        if form.is_valid():
            question = form.save()
            user = Profile.objects.get(user=request.user)
            user.rating += 1
            user.save()
            tags = form.cleaned_data.get('tags')
            for t in tags.replace(" ", "").split(","):
                if not t:
                    continue
                try:
                    tag = Tag.objects.get(text=t)
                except Tag.DoesNotExist:
                    tag = Tag(text=t)
                    tag.save()
                question.tags.add(tag)
                question.save()
            return HttpResponseRedirect('/question/' + str(question.id))
        else:
            return render(request, 'ask.html', { 'form' : form })
    else:
		form = QuestionForm()
		return render(request, 'ask.html', { 'form' : form })




	
def signup (request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.POST:
        form = SignupForm(request.POST)
        avatar_form = AvatarForm (request.POST, request.FILES)
        if form.is_valid() and avatar_form.is_valid():
            redirect = form.cleaned_data.get('redirect', '/')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            avatar = avatar_form.cleaned_data.get('avatar')
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = Profile (user=user, avatar=avatar)
            profile.save()
            us = authenticate(username = username, password = password)
            auth_login(request, us)
            return HttpResponseRedirect(redirect)
        else:
            return render(request, 'signup.html', {'form' : form, 'avatar_form' : avatar_form })
    else:
        form = SignupForm(initial= {'redirect' : request.GET.get('next', '/')})
        avatar_form = AvatarForm()
        return render(request, 'signup.html', {'form': form, 'avatar_form' : avatar_form })




def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            redirect = form.cleaned_data.get('redirect', '/')
            if user:
                auth_login(request, user)
                if redirect == '/login/' or redirect == '/signup/':
                    redirect = '/'
                return HttpResponseRedirect (redirect)
            else:
                error = u'Неверная связка логин-пароль'
                form.redirect = redirect
                return render(request, 'login.html', {'form': form, 'error' : error })
        else:
            return render(request, 'login.html', {'form': form })

    else:
        form = LoginForm(initial= {'redirect' : request.GET.get('next', '/')} )
        return render(request, 'login.html', { 'form': form })



def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')





def rate(request):
    try:
        q_id = request.POST.get('q_id')
        question = Question.objects.get(pk=q_id)
        type = request.POST.get('type')
        user = Profile.objects.get(user=request.user)
        like = Like.objects.filter(user=user, question=question).first()

        if like is None:
            if type == '1':
                Like.objects.create(question=question, user=user)
                question.rating += 1
            else:
                Like.objects.create(question=question, user=user, is_like=False)
                question.rating -= 1

        elif like.is_like != int(type):
            if like.is_like:
                question.rating -= 1
            else:
                question.rating += 1
            like.delete()

        question.save()
        return HttpResponse(json.dumps({
            'status' : 'OK',
            'likes' : question.rating,
        }), content_type='application/json')


    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'info' : str(e),
        }), content_type='application/json')







def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.POST:
        form = UpdateProfileForm(request.POST, instance=request.user)
        avatar_form = AvatarEditForm (request.POST, request.FILES)
        if form.is_valid() and avatar_form.is_valid():
            form.save()
            avatar = avatar_form.cleaned_data.get('avatar', None)
            if avatar is not None:
                p = Profile.objects.get(user=request.user)
                p.avatar = avatar
                p.save()
            return HttpResponseRedirect('/login')
        else:
            return render(request, 'profile.html', {'form' : form, 'avatar_form' : avatar_form })
    else:

        form = UpdateProfileForm(instance=request.user)
        avatar_form = AvatarEditForm()
        return render(request, 'profile.html', {'form': form, 'avatar_form' : avatar_form })


def user(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'user.html', {'user' : user })






def correct_answer (request):
    try:
        q_id = request.POST.get('q_id')
        question = Question.objects.get(pk=q_id)
        a_id = request.POST.get('a_id')
        old_id = question.correct_answer
        answer = Answer.objects.get(pk=a_id)

        if int(a_id) == old_id:
            answer.is_correct = False
            question.correct_answer = -1
        else:
            question.correct_answer = a_id
            answer.is_correct = True
            if old_id != -1:
                old_answer = Answer.objects.get(pk=old_id)
                old_answer.is_correct = False
                old_answer.save()

        answer.save()
        question.save()

        return HttpResponse(json.dumps({
            'status': 'OK',
             'old_id' : old_id,
        }), content_type='application/json')


    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'info': str(e),
        }), content_type='application/json')




	

	







