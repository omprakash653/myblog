from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    #return HttpResponse('This is home')
    return render(request, 'home/home.html')

def about(request):
    #return HttpResponse('This is about')
    return render(request, 'home/about.html')
def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        if len(name)<2 or len(email)<5 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill your form correctly")
        else:
            messages.success(request, "form submission success")
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
        
        
    return render(request, 'home/contact.html')

def search(request):
    query=request.GET['querry']
    allPostsTitle = Post.objects.filter(title__icontains=query)
    allPostsAuthor = Post.objects.filter(author__icontains=query)
    allPostsContent = Post.objects.filter(content__icontains=query)
    allPosts =  allPostsTitle.union(allPostsContent, allPostsAuthor)
    
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please filter your query.")
    params={'allPosts': allPosts}
    return render(request, 'home/search.html', params)


def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        name=request.POST['name']
        password1=request.POST['password1']
        password2=request.POST['password2']

        # check for errorneous input
        if len(username)>10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (password1!= password2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, password1)
        myuser.name= name
        myuser.save()
        messages.success(request, "Your iCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")

def handleLogin(request):
    if request.method=="POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "successfully loggedin")
            return redirect('home')
        else:
            messages.error(request, "invalid password, try again")
            return redirect('home')

    return HttpResponse('not found')

def handleLogout(request):
    logout(request)
    messages.success(request, "successfully loggedout")
    return redirect('home')

