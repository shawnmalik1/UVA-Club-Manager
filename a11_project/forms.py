# forms.py
from django import forms
from .models import Club, Event
from .models import Suggestion
from .models import Document
from .models import Project
from .models import ChatMessage
from .models import Expenditure

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description', 'points']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date']

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['suggestion_text']
        widgets = {
            'suggestion_text': forms.Textarea(attrs={'rows': 5}),
        }
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'keywords', 'file']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'file']

#This was meant for the live chat feature
class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Type your message...'})
        }

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['amount', 'description']  # Fields you want in the form

    amount = forms.DecimalField(
        max_digits=7, 
        decimal_places=2, 
        label="Expenditure Amount", 
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount'})
    )
    description = forms.CharField(
        max_length=255, 
        label="Description", 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Optional description'})
    )