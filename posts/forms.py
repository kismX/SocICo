from django import forms
from .models import Post, Event

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image', 'link', 'event']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        image = cleaned_data.get("image")
        link = cleaned_data.get("link")
        event = cleaned_data.get("event")

        if not (text or image or link or event):
            raise forms.ValidationError("Der Post muss mindestens einen Inhaltstyp enthalten.")

        return cleaned_data
    

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'location', 'image']