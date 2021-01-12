from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime as dt


# Create your views here.
def signup(request):
    if request.user.is_authenticated():
        return redirect('insta')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                new_profile = Profile(user=user)
        else:
            form = SignupForm()
    return render(request, 'registration/registration.html',{'form':form})

@login_required(login_url='/accounts/login/')
def insta(request):
    title='Instagram'
    users = User.objects.all()
    current_user = request.user
    profile = Profile.objects.filter(user=current_user).first()
    if profile == None:
        my_profile = None
    else:
        my_profile=profile
    comments = Comment.objects.all().order_by('-date_posted')
    posts = Post.objects.all().order_by('-date_posted')
    for post in posts:
        if request.method=='POST' and 'post' in request.POST:
            posted=request.POST.get("post")
            for post in posts:
                if (int(post.id)==int(posted)):
                    post.like+=1
                    post.save()
            return redirect('insta')
    return render(request, 'index.html', {"posts": posts, 'comments':comments,'users':users,'user':current_user,'my_profile':my_profile,'title':title})


@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    profile = Profile.get_profile(current_user)
    if profile == None:
        return redirect('add_profile')
    else:
        if request.method == 'POST':
            form = NewPostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = current_user
                post.profile = profile
                post.save()
            return redirect('insta')

        else:
            form = NewPostForm()
        return render(request, 'new_post.html', {"form": form})

@login_required(login_url='/accounts/login/')
def single_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.get_comments_by_post(post_id).order_by('-date_posted')
    current_user = request.user
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = current_user
            new_comment.post = post
            new_comment.save()
            return redirect('single_post',post_id=post_id)
    if request.method=='POST' and 'post' in request.POST:
            posted=request.POST.get("post")
            for post in posts:
                if (int(post.id)==int(posted)):
                    post.like+=1
                    post.save()
            return redirect('single_post',post_id=post_id)
    else:
        form = NewCommentForm()
        
    return render(request, 'post.html', {'post':post, 'form':form,'comments':comments})    

@login_required(login_url='/accounts/login/')
def my_profile(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    count = Post.objects.filter(profile=profile).count
    comments = Comment.objects.all().order_by('-date_posted')
    posts = None
    if profile == None:
        return redirect('add_profile')
    else:
        posts = Post.get_posts_by_id(profile.id).order_by('-date_posted')
        for post in posts:
            if request.method=='POST' and 'post' in request.POST:
                posted=request.POST.get("post")
                for post in posts:
                    if (int(post.id)==int(posted)):
                        post.like+=1
                        post.save()
                return redirect('profile', profile_id=profile_id)
        return render(request, 'profile.html', {"posts": posts, "profile": profile, 'count':count,'comments':comments})

@login_required(login_url='/accounts/login/')
