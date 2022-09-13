from gettext import find
import base64
import re
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
import django.http as dhttp
import NoteTake.form as form 
import NoteTake.models as models
from django.views.decorators.csrf import csrf_exempt



def homeview(request):
    response = render(request, "home.html", {}) 
    response.set_cookie('entry','false')
    response.set_cookie('signup','false')
    try:
        request.COOKIES['login']
    except(KeyError):
        response.set_cookie('login','false')
    try:
        request.COOKIES['curruser']
        return response
    except(KeyError):
        response.set_cookie('curruser','none')
        return response

def signinpage(request):
    try:
        login = request.COOKIES['login']
        signup = request.COOKIES['signup']
        if(login=='false'):
            if(signup=='true'):
                return render(request,"notesignin.html",{'form': form.LoginnSignupForm(), 'signin_comment':'Your Sign Up Was Successful'})
            else:
                return render(request,"notesignin.html",{'form': form.LoginnSignupForm(), 'signin_comment':'To Resume Your Session'})
    except(KeyError):
        return dhttp.HttpResponse("Please Enable Cookies and try again")

def signuppage(request):
    try:
        login = request.COOKIES['login']
        if(login=='false'):
            return render(request,"notesignup.html",{'form': form.LoginnSignupForm()})
    except(KeyError):
        dhttp.HttpResponse("Please Enable Cookies and try again")
    

def logout(request):
    response = redirect("/notetake/")
    response.set_cookie('login','false')
    response.set_cookie('curruser','none')
    return response

def noteview(request):
    try:
        login = request.COOKIES['login']
        if(login=='true'):
            return render(request,"notesearch.html", {}) # only parsing this form so that the csrf token is valid
        else:
            return redirect("/notetake/signinpage")
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
            return redirect("/notetake/signinpage")
    except(KeyError):
        return dhttp.HttpResponse("Please enable cookies and try again") 

def signup(request):
    if(request.method=="POST"):
        signupform = form.LoginnSignupForm(request.POST)
        newuser = models.User()
        if signupform.is_valid():
            newuser.username = signupform.cleaned_data['username']
            newuser.password = signupform.cleaned_data['password']
            newuser.userid = str(base64.b64encode(newuser.username.encode("ascii")))[2:-1]
        else:
            response = dhttp.HttpResponse("Form not valid")
            response.set_cookie('signup','true')
            return response
        
        newuser.save()
        response = redirect('./signinpage')
        response.set_cookie('signup','true')
        return response

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
                response = redirect("/notetake/")
                response.set_cookie('login','true')
                response.set_cookie('curruser',find_user.userid)
                return response
            else:
                return render(request,"notesignin.html",{'form': form.LoginnSignupForm(), 'signin_error':'Please Check the Fields and try again', 'signin_comment':'To Resume Your Session'})
        except:
            return render(request,"notesignin.html",{'form': form.LoginnSignupForm(), 'signin_error':'Please Check the Fields and try again', 'signin_comment':'To Resume Your Session'})

def takenote(request):
    noteform = form.NoteForm(request.POST)
    newnote = models.Note()
    if noteform.is_valid():
        newnote.date = noteform.cleaned_data['date']
        newnote.title = noteform.cleaned_data['title']
        newnote.text = noteform.cleaned_data['text']
        newnote.userid = request.COOKIES['curruser']
    else:
        return dhttp.HttpResponse("Form not valid")
    newnote.save()
    response = redirect("./notesenter")
    response.set_cookie('entry','true')
    return response

@csrf_exempt # for getting the input field data without passing a form
def searchnote(request):
    search_query = request.POST['title'] #retrieving like this because I used a from but not with both fields (could've used JS to populate both fields)
    queryarr = search_query.split('%')
    notes = {'title':'default','date':'default'}
    if(queryarr[0]=='title'):
        title_query = queryarr[1]
        limit = int(queryarr[2])
        userid = request.COOKIES['curruser']
        notes = (models.Note.objects.filter(userid=userid) & models.Note.objects.order_by('date').filter(title__startswith = title_query))[:limit]
    elif(queryarr[0]=='date'):
        date_query = queryarr[1]
        limit = int(queryarr[2])
        userid = request.COOKIES['curruser']
        notes = (models.Note.objects.filter(userid=userid) & models.Note.objects.order_by('date').filter(date__startswith = date_query))[:limit]
    resp = ''
    for x in notes:
        resp += '<li><form method="POST" action="/notetake/viewnote">'
        # respend = 
        resp += '<input type="text" value="'+x.date+'" readonly="true" name="date" hidden="true">'
        resp += '<input type="text" value="'+x.title+'" readonly="true" name="title" hidden="true"><input type="submit" value="'+x.title+str(" -- Taken On -- ")+x.date+'"class="resformfieldinner">' 
        resp+= '</form></li>'
    return render(request,'notesearch.html',{'results':resp})

@csrf_exempt
def viewnote(request):
    # print(request.POST)
    qtitle = request.POST.get('title','NONE')
    qdate = request.POST.get('date','NONE')
    note = models.Note.objects.filter(title=qtitle) & models.Note.objects.filter(date=qdate)
    # print(qtitle,qdate)
    # print(note[0].date)
    notedict = {'date':note[0].date,'title':note[0].title,'text':note[0].text}
    return render(request,'notedisplay.html',{'form':form.NoteForm(notedict)}) 