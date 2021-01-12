from django import forms
from .models import Profile, Post, Comment, Follow

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'date_posted','profile','like']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post', 'user', 'date_posted']