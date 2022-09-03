from gettext import find
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
import django.http as dhttp
import NoteTake.form as form 
import NoteTake.models as models

# will create a function checksignedin to see if the user is signed in using cookie, else will redirect to the signin page
# format will be like home-> note enter or view will invoke the cookie check, if not found redirect to sign in page then after successful signin return home.

def homeview(request):
    return render(request, "home.html", {})

def signinpage(request):
    return render(request,"notesignin.html",{'form': form.LoginnSignupForm()})

def signuppage(request):
    return render(request,"notesignup.html",{'form': form.LoginnSignupForm()})

def logout(request):
    response = redirect("http://localhost:8000/notetake/")
    response.delete_cookie('login')
    return response

def noteview(request):
    try:
        login = request.COOKIES['login']
        if(login=='true'):
            return render(request,"noteview.html", {})
    except(KeyError):
        return redirect("http://localhost:8000/notetake/signinpage")

def noteenter(request):
    try:
        login = request.COOKIES['login']
        if(login=='true'):
            return render(request,"notetake.html", {'form':form.NoteForm()})
    except(KeyError):
        return redirect("http://localhost:8000/notetake/signinpage")

def signup(request):
    if(request.method=="POST"):
        signupform = form.LoginnSignupForm(request.POST)
        newuser = models.User()
        if signupform.is_valid():
            newuser.username = signupform.cleaned_data['username']
            newuser.password = signupform.cleaned_data['password']
        else:
            return dhttp.HttpResponse("Form not valid")
        newuser.save()
        return dhttp.HttpResponse("Sign Up Successful now sign in")

def signin(request):
    if(request.method == "POST"):
        signinform = form.LoginnSignupForm(request.POST)
        user = models.User()
        if signinform.is_valid():
            user.username = signinform.cleaned_data['username']
            user.password = signinform.cleaned_data['password']
        else:
            return dhttp.HttpResponse("Form not valid")
        find_user = ''
        try:
            find_user = models.User.objects.get(username=user.username)
            if(user.password == find_user.password):
                response = redirect("http://localhost:8000/notetake/")
                response.set_cookie('login','true')
                return response
            else:
                return dhttp.HttpResponse("Password Mismatch")
        except:
            return dhttp.HttpResponse("User Not Found")

