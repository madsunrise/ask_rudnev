from django import template
from my_app.models import Tag, Profile
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('best.html')
def best():
    data = cache.get('best')
    if not data:
        tags = Tag.objects.top()
        users = Profile.objects.top()
        data = { 'tags' : tags, 'users' : users }
        cache.set('best', data, 15 * 60)
    return { 'data' : data }