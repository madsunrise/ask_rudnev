from django.conf.urls import patterns, url
from my_app import views as ask_views

urlpatterns = [
    url(r'^login/', ask_views.login, name='login'),
    url(r'^logout/', ask_views.logout, name='logout'),
    url(r'^signup/', ask_views.signup, name='signup'),
    url(r'^ask/', ask_views.ask, name='ask'),
    url(r'^top/', ask_views.top, name='top'),
    url(r'^rate/', ask_views.rate, name='rate'),
    url(r'^correct_answer/', ask_views.correct_answer, name='correct_answer'),
    url(r'^profile/', ask_views.profile, name='profile'),
    url(r'^question/(?P<question_id>\d+)/$', ask_views.question, name='question'),
    url(r'^tag/(?P<tag_id>\d+)/$', ask_views.tag, name='tag'),
    url(r'^user/(?P<user_id>\d+)/$', ask_views.user, name='user'),
    url(r'^$', ask_views.index, name='index'),
]
