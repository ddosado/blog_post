from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post
from .forms import CommentForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.http import HttpResponseRedirect

   
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

#class PostDetail(generic.DetailView):
#    model = Post
#    template_name = 'post_detail.html'
    
def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
                                           
def about(request):
    return render(request, 'about.html')

def picture(request):
    return render(request, 'picture.html')


##################################################################
def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse_lazy('blog:home'))
	else:
		return HttpResponseRedirect(reverse_lazy('auth_login'))
