from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime as dt
from .models import Profile, Post, Comment, Follow
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm, PostForm, CommentForm
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
    comments = Comment.objects.all().order_by('-date_posted')
    posts = Post.objects.all().order_by('-date_posted')
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
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = current_user
                post.profile = profile
                post.save()
            return redirect('insta')

        else:
            form = PostForm()
        return render(request, 'newPost.html', {"form": form})

@login_required(login_url='/accounts/login/')
def single_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.get_comments_by_post(post_id).order_by('-date_posted')
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
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
        form = CommentForm()
        
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
def our_profile(request):
    our_user = request.user
    profile = Profile.objects.get(user=our_user)
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

def update_post(request,post_id):
    post= Post.objects.get(pk=post_id).order_by('-date_posted')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.caption=form_data.cleaned_data[caption]
            post=post.update_post(post_id,caption)
            return redirect('my_profile')
    else:
        form = PostForm()
    return render(request, 'postUpdate.html',{'form':form,'post':post})

def delete_post(request,post_id):
    post= Post.objects.get(pk=post_id)
    post.delete_post()
    return redirect('my_profile')
    return render(request, 'my_profile')


@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    profile = Profile.get_profile(current_user)
    if profile == None:
        return redirect('add_profile')
    else:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = current_user
                post.profile = profile
                post.save()
            return redirect('insta')

        else:
            form = PostForm()
        return render(request, 'newPost.html', {"form": form})

@login_required(login_url='/accounts/login/')
def add_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = current_user
            new_profile.save()
        return redirect('my_profile')

    else:
        form = ProfileForm()
    return render(request, 'addProfile.html', {"form": form})

@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = current_user
            new_profile.save()
        return redirect('my_profile')

    else:
        form = ProfileForm()
    return render(request, 'addProfile.html', {"form": form})

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'user' in request.GET and request.GET["user"]:
        search_term = request.GET.get("user")
        profiles = Profile.find_profile(search_term)
        message = f"{search_term}"
        
        return render(request, 'search.html',{"results": profiles, "message":message})

    else:
        message = "No searches yet!"
        return render(request, 'search.html',{"message":message})

@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    profile = Profile.get_profile_id(profile_id)
    posts = Post.objects.filter(profile=profile.id).order_by('-date_posted')
    count = Post.objects.filter(profile=profile).count
    comments = Comment.objects.all().order_by('-date_posted')
    for post in posts:
        if request.method=='POST' and 'post' in request.POST:
            posted=request.POST.get("post")
            for post in posts:
                if (int(post.id)==int(posted)):
                    post.like+=1
                    post.save()
            return redirect('profile', profile_id=profile_id)
    return render(request, 'userProfile.html', {"posts": posts, "profile": profile, 'count':count,'comments':comments})


@login_required(login_url='/accounts/login/')
def follow(request, profile_id):
    current_user = request.user
    profile = Profile.get_profile_id(profile_id)
    follow_user = Follow(user=current_user, profile=profile)
    follow_user.save()
    myprofile_id= str(profile.id)
    return redirect('insta')