from django import forms
import NoteTake.models as models

class LoginnSignupForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields  = ('username','password')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'formfieldinner','id':'username','autocomplete':'off'}),
            'password' : forms.PasswordInput(attrs={'class':'formfieldinner','id':'password'})
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ('date','title','text')
        widgets = {
            'date' : forms.TextInput(attrs={'class':'formfieldinner','id':'currdate'}),
            'title': forms.TextInput(attrs={'class':'formfieldinner','placeholder':'Title','autocomplete':'off'}),
            'text': forms.Textarea(attrs={'placeholder':'Enter Your Note Here...','class':'formfieldinner'})
        }
        def __init__(self,*args,**kwargs):
            self.date = kwargs.pop('date')
            self.title = kwargs.pop('title')
            self.text = kwargs.pop('text')
            super(NoteForm, self).__init__(*args,**kwargs)
            self.fields['date'].widget = forms.TextInput(attrs={'class':'formfieldinner','id':'currdate','readonly':'true','value':self.date})
            self.fields['text'].widget = forms.Textarea(attrs={'readonly':'true','id':'currtext','value':self.text})
            self.field['title'].widget = forms.TextInput(attrs={'class':'formfieldinner','readonly':'true','id':'currtitle','value':self.title})