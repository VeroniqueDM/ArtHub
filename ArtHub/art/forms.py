from django import forms

from ArtHub.art.models import ArtPiece, News, Event, Style, Technique
from ArtHub.art.views_mixins import BootstrapFormMixin

'''
THIS IS FOR CREATE ART FORM
'''


# styles = forms.ModelMultipleChoiceField(
#     queryset=Style.objects.all(),
#     widget=forms.CheckboxSelectMultiple,
# )
# techniques = forms.ModelMultipleChoiceField(
#     queryset=Technique.objects.all(),
#     widget=forms.CheckboxSelectMultiple,
# )
class CreateArtForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        # self.user = user

    # def save(self, commit=True):
    #     art = super().save(commit=False)
    #     # art.user = self.user
    #     if commit:
    #         art.save()
    #     return art

    class Meta:
        model = ArtPiece
        fields = ('title', 'photo', 'description', 'style', 'technique', 'medium_used', 'type')
        widgets = {
            # 'style': forms.CheckboxSelectMultiple,
            # 'technique': forms.CheckboxSelectMultiple,
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
        exclude = ('title', 'liked_by','photo', 'description', 'publication_date', 'user', 'style', 'technique', 'medium_used', 'likes' )



class CreateNewsForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.user = user

    def save(self, commit=True):
        # commit false does not persist to database
        # just returns the object to be created
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

    class Meta:
        model = ArtPiece
        fields = ('title', 'photo', 'description', 'style', 'technique', 'medium_used')


class CreateStyleForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Style
        fields = ('name', 'description', 'photo')



class CreateTechniqueForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()



    class Meta:
        model = Technique
        fields = ('name', 'description', 'photo')


class EditStyleForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()


    class Meta:
        model = Style
        fields = ('photo', 'name', 'description')


class EditTechniqueForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()


    class Meta:
        model = Technique
        fields = ('photo', 'name', 'description')
