from django import forms
from django.core.exceptions import ValidationError

from ArtHub.art.models import ArtPiece, News, Event, Style, Technique
from ArtHub.art.views_mixins import BootstrapFormMixin


class CreateArtForm(BootstrapFormMixin, forms.ModelForm):
    style = forms.ModelMultipleChoiceField(
        queryset=Style.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    technique = forms.ModelMultipleChoiceField(
        queryset=Technique.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    max_upload_limit = 5 * 1024 * 1024

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('photo')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('photo', f"File must be < 5 MB")

    class Meta:
        model = ArtPiece
        fields = ('title', 'photo', 'description', 'style', 'technique', 'medium_used', 'type')
        widgets = {
            # 'style': forms.CheckboxSelectMultiple,
            # 'technique': forms.CheckboxSelectMultiple,
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title of your art'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your art piece'}),
            'style': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'technique': forms.SelectMultiple(attrs={'class': 'form-control'}),
            # 'style': forms.CheckboxSelectMultiple(),
            # 'technique': forms.CheckboxSelectMultiple(),
            'medium_used': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. glass, paint, charcoal..'
                }
            ),
            'type': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. drawing, sculpture..'
                }
            )
        }
        labels = {
            'category': 'Select Categories',
            'type': 'Type of Art'
        }


class DeleteArtForm(forms.ModelForm):

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = ArtPiece
        exclude = ('title', 'liked_by','photo', 'description', 'publication_date', 'user', 'style', 'technique', 'medium_used', 'likes', 'type' )



class CreateNewsForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.user = user

    def save(self, commit=True):
        news = super().save(commit=False)

        news.user = self.user
        if commit:
            news.save()

        return news

    class Meta:
        model = News
        fields = ('title', 'subtitle', 'content', 'photo')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Title',
                }
            ),
            'photo': forms.TextInput(
                attrs={
                    'placeholder': 'Enter URL',
                }
            ),
            'subtitle': forms.TextInput(attrs={'placeholder': 'Enter Subtitle'}),
            'content': forms.Textarea(attrs={'placeholder': 'Enter Content'}),
        }


class CreateEventForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.user = user

    def save(self, commit=True):

        event = super().save(commit=False)

        event.user = self.user
        if commit:
            event.save()

        return event

    class Meta:
        model = Event
        fields = ('title', 'description', 'location', 'date', 'price', 'photo' )
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Title',
                }
            ),
        }


class EditEventForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Event
        fields = ('title', 'description', 'location', 'date', 'price', 'photo')


class EditNewsForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = News
        fields = ('title', 'subtitle', 'content', 'photo', )


class EditArtForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    max_upload_limit = 5 * 1024 * 1024

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('photo')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('photo', f"File must be < 5 MB")

    class Meta:
        model = ArtPiece
        fields = ('title', 'photo', 'description', 'style', 'technique', 'medium_used')


class CreateStyleForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['photo'].widget.attrs['placeholder'] = 'Enter Photo URL'

    max_upload_limit = 5 * 1024 * 1024

    def clean_name(self):
        name = self.cleaned_data['name']
        if Style.objects.filter(name=name).count() > 0:
            raise ValidationError('This style was already added.')
        return name

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('photo')
        if pic is None:
            self.add_error('photo', 'Please add a photo')
        if len(pic) > self.max_upload_limit:
            self.add_error('photo', f"File must be < 5 MB")

    class Meta:
        model = Style
        fields = ('name', 'description', 'photo')


class CreateTechniqueForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['photo'].widget.attrs['placeholder'] = 'Enter Photo URL'

    max_upload_limit = 5 * 1024 * 1024

    def clean_name(self):
        name = self.cleaned_data['name']
        if Technique.objects.filter(name=name).count() > 0:
            raise ValidationError('This technique was already added.')
        return name

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('photo')
        if pic is None:
            self.add_error('photo', 'Please add a photo')
        if len(pic) > self.max_upload_limit:
            self.add_error('photo', f"File size must be < 5 MB")

    class Meta:
        model = Technique
        fields = ('name', 'description', 'photo')


class EditStyleForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['photo'].widget.attrs['placeholder'] = 'Enter Photo URL'

    max_upload_limit = 5 * 1024 * 1024

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('photo')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('photo', f"File must be < 5 MB")

    class Meta:
        model = Style
        fields = ('photo', 'name', 'description')


class EditTechniqueForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    max_upload_limit = 5 * 1024 * 1024

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('photo')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('photo', f"File must be < 5 MB")

    class Meta:
        model = Technique
        fields = ('photo', 'name', 'description')
