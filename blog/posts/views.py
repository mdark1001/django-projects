from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailForm, CommentForm

from .models import Post
from taggit.models import Tag


# Create your views here.

def post_list(request, tag_slug=None):
    """

    """
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        print(tag)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 10)  #
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except  PageNotAnInteger:
        posts = paginator.page(1)
    except  EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    """

    """
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List active coments by post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    # Se incluye un método para obtener los post similares.
    # list similar post
    post_tags_ids = post.tags.values_list('id', flat=True)  # values_list return tuples whit values for the given fields
    similar_post = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)  # excluye el post actual
    print(similar_post)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    print(similar_post)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_post': similar_post,
                   })


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Send Email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} f{cd['name']} comments: {cd['comments']}"
            send_mail(subject, message, 'admin@miblog.com', [cd['to']])
            sent = True
    else:
        form = EmailForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


class PostListView(ListView):
    """ Class base view """

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 1
    template_name = 'blog/post/list.html'
