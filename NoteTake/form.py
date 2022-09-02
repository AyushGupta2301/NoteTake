from django import forms
import NoteTake.models as models

class LoginnSignupForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields  = ('username','password')
        widgets = {
            'username' : forms.TextInput(),
            'password' : forms.PasswordInput()
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ('date','title','text')
        widgets = {
            'date' : forms.DateInput(),
            'title': forms.TextInput(),
            'text':forms.Textarea()
        }