from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# Create your views here.


class PostList(generic.ListView):
    """ A view for the post list """
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "events/posts.html"
    paginate_by = 6


class PostDetail(View):
    """ A view for the post detail """
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "events/post_detail.html",
            {
                "post": post,
                "liked": liked,
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "liked": liked
            },
        )


class PostLike(View):
    """ A view for the post likes """
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


@login_required
def add_post(request):
    """ Add a post to the events page """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added post!')
            return redirect('posts')
        else:
            messages.error(request, 'Failed to add post. Please ensure the form is valid.')
    else:
        form = PostForm()

    template = 'events/add_post.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_post(request, slug, *args, **kwargs):
    """ Edit a post in the events section """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('post_detail', args=[slug]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = PostForm(instance=post)
        messages.info(request, f'You are editing {post.title}')

    template = 'events/edit_post.html'
    context = {
        'form': form,
        'post': post,
    }

    return render(request, template, context)


@login_required
def delete_post(request, slug, *args, **kwargs):
    """ Delete post from events page """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    post.delete()
    messages.success(request, 'Post deleted!')
    return redirect(reverse('posts'))
