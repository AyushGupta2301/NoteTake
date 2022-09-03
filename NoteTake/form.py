from django import forms
import NoteTake.models as models

class LoginnSignupForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields  = ('username','password')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'formfieldinner'}),
            'password' : forms.PasswordInput(attrs={'class':'formfieldinner'})
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ('date','title','text')
        widgets = {
            'date' : forms.TextInput(attrs={'class':'formfieldinner','id':'currdate'}),
            'title': forms.TextInput(attrs={'class':'formfieldinner','placeholder':'Title'}),
            'text': forms.Textarea(attrs={'placeholder':'Enter Your Note Here...'})
        }