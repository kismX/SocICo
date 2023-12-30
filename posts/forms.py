from django import forms
from .models import Post, Event, Comment


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
            raise forms.ValidationError("Der Post muss mindestens irgendwas enthalten!")

        return cleaned_data
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'image', 'link']

    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data.get("comment")
        image = cleaned_data.get("image")
        link = cleaned_data.get("link")

        if not (comment or image or link):
            raise forms.ValidationError("Der Post muss wenigstens irgendwas enthalten.")

        return cleaned_data


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'location', 'image']
        widgets = {
            'start_time': forms.SplitDateTimeWidget(date_attrs={'type': 'date'}, time_attrs={'type': 'time'}),
            'end_time': forms.SplitDateTimeWidget(date_attrs={'type': 'date'}, time_attrs={'type': 'time'}),
        }