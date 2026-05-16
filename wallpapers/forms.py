from django import forms


class WallpaperUploadForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    tags = forms.CharField(required=False, help_text='Comma-separated tags')
    category = forms.CharField(max_length=100, required=False)
    is_featured = forms.BooleanField(required=False)
    file = forms.ImageField(required=True)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
