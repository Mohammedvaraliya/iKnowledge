from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.

# HTML Pages
def home(request): 
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    return render(request, "home/home.html", context)

def about(request): 
    return render(request, "home/about.html")

def contact(request):
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")

    return render(request, "home/contact.html")

def search(request):
    query = request.GET['query']

    if len(query) > 78:
        allPosts = Post.objects.none()

    else:
        allPostsTitle = Post.objects.filter(title__icontains = query)
        allPostsDiscription = Post.objects.filter(discription__icontains = query)
        allPostsContent = Post.objects.filter(content__icontains = query)
        allPostsAuthor = Post.objects.filter(author__icontains = query)
        allPosts = allPostsTitle.union(allPostsDiscription, allPostsContent, allPostsAuthor)

    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query")

    params = {'allPosts': allPosts, 'query': query}
    return render(request, "home/search.html", params)

# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # check the errorneos inputs
        if len(username) > 25:
            messages.error(request, "Username must be under 25 characters SignUp again!!!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers SignUp again!!!")
            return redirect('home')

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'Username already exists try different username And SIgnUp again!!!')
            return redirect('home')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already exists try different Email And SignUp again!!!')
            return redirect('home')

        if password1 != password2:
            messages.error(request, "Passwords do not match SignUp again!!!")
            return redirect('home')


        # Create the user
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created!")
        return redirect('home')

    else:
        return HttpResponse("404 - Not Found")

def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "You Have Successfully Logged In!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')

    return HttpResponse("404 - Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request, "You Have Successfully Logged Out!")
    return redirect('home')

