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
            'date' : forms.DateInput(attrs={'class':'formfieldinner'}),
            'title': forms.TextInput(attrs={'class':'formfieldinner'}),
            'text':forms.Textarea(attrs={'class':'formfieldinner'})
        }