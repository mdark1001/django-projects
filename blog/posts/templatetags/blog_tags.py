"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 16/08/21
@name: blog_tags
"""
from django import template
from ..models import Post

register = template.Library()


@register.simple_tag(name='get_total_posts')
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def get_last_post(count):
    post = Post.published.order_by('-publish')[:count]
    return {'latest_posts': post}
