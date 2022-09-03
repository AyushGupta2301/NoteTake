from gettext import find
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
import django.http as dhttp
import NoteTake.form as form 
import NoteTake.models as models



def homeview(request):
    response = render(request, "home.html", {}) 
    response.set_cookie('entry','false')
    try:
        request.COOKIES['login']
        return response
    except(KeyError):
        response.set_cookie('login','false')
        return response

def signinpage(request):
    try:
        login = request.COOKIES['login']
        if(login=='false'):
            return render(request,"notesignin.html",{'form': form.LoginnSignupForm()})
    except(KeyError):
        dhttp.HttpResponse("Please Enable Cookies and try again")

def signuppage(request):
    try:
        login = request.COOKIES['login']
        if(login=='false'):
            return render(request,"notesignup.html",{'form': form.LoginnSignupForm()})
    except(KeyError):
        dhttp.HttpResponse("Please Enable Cookies and try again")
    

def logout(request):
    response = redirect("http://localhost:8000/notetake/")
    response.set_cookie('login','false')
    return response

def noteview(request):
    try:
        login = request.COOKIES['login']
        if(login=='true'):
            return render(request,"noteview.html", {})
        else:
            return redirect("http://localhost:8000/notetake/signinpage")
    except(KeyError):
        return dhttp.HttpResponse("Please enable cookies and try again")

def noteenter(request):
    try:
        login = request.COOKIES['login']
        if(login=='true'):
            if(request.COOKIES['entry']=='false'):
                return render(request,"notetake.html", {'form':form.NoteForm(),'note_entry':'Enter Notes, Have Fun'})
            else:
                return render(request,"notetake.html", {'form':form.NoteForm(),'note_entry':'Note Taken Successfully :)'})
        else:
            return redirect("http://localhost:8000/notetake/signinpage")
    except(KeyError):
        return dhttp.HttpResponse("Please enable cookies and try again") 

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

def takenote(request):
    noteform = form.NoteForm(request.POST)
    newnote = models.Note()
    if noteform.is_valid():
        newnote.date = noteform.cleaned_data['date']
        newnote.title = noteform.cleaned_data['title']
        newnote.text = noteform.cleaned_data['text']
    else:
        return dhttp.HttpResponse("Form not valid")
    newnote.save()
    response = redirect("./notesenter")
    response.set_cookie('entry','true')
    return response

