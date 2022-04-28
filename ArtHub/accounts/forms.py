from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from ArtHub.accounts.models import UserProfile, ArtHubUser
from ArtHub.accounts.views_mixins import DisabledFieldsFormMixin
from ArtHub.art.models import ArtPiece
from ArtHub.art.views_mixins import BootstrapFormMixin
UserModel = get_user_model()

class CreateRegularProfileForm(BootstrapFormMixin,UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    first_name = forms.CharField(
        max_length=UserProfile.FIRST_NAME_MAX_LENGTH,
    )
    last_name = forms.CharField(
        max_length=UserProfile.LAST_NAME_MAX_LENGTH,
    )
    profile_photo = forms.ImageField(

    )
    date_of_birth = forms.DateField()
    email = forms.EmailField()
    type = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"required": True}),
        choices=ArtHubUser.Types.choices,
        required=True,
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'type',
                  'first_name', 'last_name', 'profile_photo'
                  )
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),
        }

    def save(self, commit=True):
        # user.type = self.cleaned_data['type']

        user = super().save(commit=commit)
        profile = UserProfile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            profile_photo=self.cleaned_data['profile_photo'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            email=self.cleaned_data['email'],
            user=user,
        )
        if commit:
            profile.save()

        # if profile.is_artist == 'Artist':
        #     user.user_permissions.add(
        #
        #     )
        return user


# class CreateArtistProfileForm(CreateRegularProfileForm):

class RegularProfileUpdateForm(BootstrapFormMixin,forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    profile_photo = forms.ImageField(

    )
    # styles = forms.
    # MAYBE FIX THIS
    date_of_birth = forms.DateField(widget=forms.TextInput, disabled=True)
    email = forms.EmailField(

    )
    description = forms.TextInput(

    )

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'profile_photo', 'date_of_birth', 'email', 'description']


class DeleteProfileForm(DisabledFieldsFormMixin, BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_disabled_fields()
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        # ArtPiece.objects.filter(user_id=self.instance.pk).delete()
        # profile = self.instance
        # own_art = self.instance.art_piece__set
        user = ArtHubUser.objects.get(pk=self.instance.pk)
        own_art = user.art_piece__set
        own_art.delete()
        own_events = user.event_set
        own_events.delete()
        # profile = UserProfile.objects.get(pk=self.instance.pk)
        user.delete()
        self.instance.delete()
        return self.instance

    class Meta:
        model = UserProfile
        exclude = ('user', 'description', 'profile_photo', 'first_name', 'last_name', 'date_of_birth', 'email', )


