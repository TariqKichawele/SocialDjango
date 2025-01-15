from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

def home(request):
    post = Post.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user=request.user)

    context = {
        'post': post,
        'profile': profile
    }
    return render(request, 'main.html', context)

def signup(request):
    try:
        if request.method == 'POST':
            fnm = request.POST.get('fnm')
            emailid = request.POST.get('emailid')
            pwd = request.POST.get('pwd')

            my_user = User.objects.create_user(fnm, emailid, pwd)
            my_user.save()

            user_model = User.objects.get(username=fnm)

            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()

            if my_user is not None:
                login(request, my_user)
                return redirect("/")
            return redirect("/loginn")
    except Exception as e:
        invalid = "User already exists"
        return render(request, 'signup.html', {'invalid': invalid})
    
    return render(request, 'signup.html')

def loginn(request):

    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
       
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request, userr)
            return redirect("/")
        
        invalid = "Invalid username or password"
        return render(request, 'loginn.html', {'invalid': invalid})
    return render(request, 'loginn.html')


@login_required(login_url='/loginn')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect("/")
    else:
        return redirect("/")
    

@login_required(login_url='/loginn')
def likes(request, id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id)

        like_filter = LikePost.objects.filter(post_id=id, username=username).first()

        if like_filter == None:
            new_like = LikePost.objects.create(post_id=id, username=username)
            post.no_of_likes = post.no_of_likes + 1
        else:
            like_filter.delete()
            post.no_of_likes = post.no_of_likes - 1

        post.save()

        print(post.id)

        return redirect("/#" + id)

def home_post(request, id):
    post = Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)

    context = {
        'post': post,
        'profile': profile
    }
    return render(request, 'main.html', context)

@login_required(login_url='/loginn')
def explore(request):
    post = Post.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user=request.user)

    context = {
        'post': post,
        'profile': profile
    }
    return render(request, 'explore.html', context)

@login_required(login_url='/loginn')
def profile(request, id_user):
    user_object = User.objects.get(username=id_user)
    print(user_object)

    profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=id_user).order_by('-created_at')

    user_posts_length = len(user_posts)

    follower = request.user.username
    user = id_user

    if Followers.objects.filter(follower=follower, user=user).first():
        follow_unfollow = 'Unfollow'
    else:
        follow_unfollow = 'Follow'

    user_followers = len(Followers.objects.filter(user=id_user))
    user_following = len(Followers.objects.filter(follower=id_user))

    context = {
        'user_object': user_object,
        'profile': profile,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_posts_length': user_posts_length,
        'follow_unfollow': follow_unfollow,
        'user_followers': user_followers,
        'user_following': user_following,
    }

    if request.user.username == id_user:
        if request.method == 'POST':
            if request.FILES.get('image') == None:
                image = user_profile.profileImg
                bio = request.POST['bio']
                location = request.POST['location']

                user_profile.profileImg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()

            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                bio = request.POST['bio']
                location = request.POST['location']

                user_profile.profileImg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()

                return redirect('/profile/' + id_user)
            else:
                return render(request, 'profile.html', context)
    
    return render(request, 'profile.html', context)

def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return redirect('/')
    
@login_required(login_url='/loginn')
def search_results(request):
    query = request.GET.get('q')

    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)

    context = {
        'users': users,
        'posts': posts,
        'query': query
    }

    return render(request, 'search_user.html', context)

@login_required(login_url='/loginn')
def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()

    return redirect('/profile/' + request.user.username)


def logoutt(request):
    logout(request)
    return redirect("/loginn")
