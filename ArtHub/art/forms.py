from django import forms

from ArtHub.art.models import ArtPiece, News, Event

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

class DeleteArtForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = ArtPiece
        exclude = ('title', 'photo', 'description', 'publication_date', 'user', 'style', 'technique', 'medium_used', 'likes' )



class CreateNewsForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
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


class CreateEventForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
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