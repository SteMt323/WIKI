from django import forms

class NewWiki(forms.Form):
    title = forms.CharField(label="Titulo", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.CharField(label="Category", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label="Autor", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label= "Contenido (MD)", widget=forms.Textarea(attrs={'class':'form-control','rows':10}))
    image = forms.ImageField(label="Imagen", required=False)