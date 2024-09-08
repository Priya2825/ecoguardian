from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Blog, Subscriber, Comment
from blog.forms import BlogForm, LoggedUserCommentForm, GuestUserCommentForm
from django.core.mail import send_mail
from django.contrib import messages


# Create your views here.
def create_blog(request):
    context = {}
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit= False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created successfully!')
            return redirect('list-blogs')
        else:
            messages.error(request, 'Error creating blog. Please try again!')
            return redirect('create-blog')
    else:
        form = BlogForm()
    context['form'] = form
    return render(request, 'create_blog.html', context)

def list_blogs(request):
    context = {}
    # for subscriber submission
    if request.method == "POST":
        email = request.POST['subscriberEmail']
        print(email, ">>>email")
        if Subscriber.objects.filter(email = email).exists() and email is not None:
            print("You have already subscribed")
            messages.info(request, "You have already subscribed")
            return redirect("list-blogs")
        else:
            subscriber = Subscriber.objects.create(email = email)
            send_mail(
                "EcoGuardian Subscription",
                "Thank you for subscribing, we will post you future news and blogs.",
                "priyaambaldhage@gmail.com",
                [subscriber.email],
                fail_silently=False,
            )
            print("You have subscribed successfully.")
            messages.success(request, 'You have subscribed successfully!')
            return redirect('subscription-success')
    else: 
        all_blogs = Blog.objects.all()
        context['blogs'] = all_blogs
        return render(request, 'list_blog.html', context)

def subscription_success(request):
    return render(request, 'success_subcription.html')

def detail_blog(request, blog_slug):
    context = {}
    blog = get_object_or_404(Blog, slug=blog_slug)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = LoggedUserCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                comment.save()
                messages.success(request, 'Thank you for commenting to this blog')
                return redirect('detail-blog', blog_slug = blog_slug)
            else:
                messages.error(request, 'Error creating comments. Please try again!')
                return redirect('detail-blog', blog_slug=blog_slug)
        else:
            form = LoggedUserCommentForm()
        context['loggeduser_form'] = form
    else:
        if request.method == 'POST':
            form = GuestUserCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.full_name = form.cleaned_data['full_name']
                comment.email = form.cleaned_data['email']
                comment.blog = blog
                comment.save()
                messages.success(request, 'Thank you for commenting to this blog')
                return redirect('detail-blog', blog_slug = blog_slug)
            else:
                messages.error(request, 'Error creating comments. Please try again!')
                return redirect('detail-blog', blog_slug=blog_slug)
        else:
            form = GuestUserCommentForm()
        context['guestuser_form'] = form
    comments = Comment.objects.filter(blog__id = blog.id).order_by('-id')
    context['comments'] = comments
    context["blog"] = blog
    return render(request, 'detail_blog.html', context)
    
def edit_blog(request, blog_slug):
    context = {}
    blog = get_object_or_404(Blog, slug=blog_slug)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit= False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog updated successfully')
            return redirect('list-blogs')
        else:
            messages.error(request, 'Error updating blog. Please try again!')
            return redirect('edit-blog', blog_slug=blog_slug)
    else:
        form = BlogForm(instance=blog)
    context['form'] = form
    return render(request, 'edit_blog.html', context)

def delete_blog(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    blog.delete()
    messages.success(request, 'Blog deleted successfully')
    return redirect('list-blogs')



