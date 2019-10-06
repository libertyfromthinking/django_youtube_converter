from django import forms


class DownloadForm(forms.Form):
    url = forms.CharField(widget=forms.TextInput(attrs={ 'id':'search_input', 'placeholder': 'Enter video or playlist url' }), label='')
