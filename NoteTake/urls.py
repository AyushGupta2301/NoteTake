"""NoteTake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import NoteTake.views as ntv 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('notetake/',ntv.homeview, name='homeview'),
    path('notetake/notesenter/',ntv.noteenter, name='notesenter'),
    path('notetake/notesview/',ntv.noteview, name='notesview'),
    path('notetake/signuppage',ntv.signuppage,name='signuppage'),
    path('notetake/signinpage',ntv.signinpage,name='signinpage'),
    path('notetake/signup',ntv.signup,name='signup'),
    path('notetake/signin',ntv.signin,name='signin'),
    path('notetake/takenote',ntv.takenote,name='takenote'),
    path('notetake/searchnote',ntv.searchnote,name='searchnote'),
    path('notetake/viewnote',ntv.viewnote,name='viewnote'),
    path('notetake/logout',ntv.logout,name='logout')
]
