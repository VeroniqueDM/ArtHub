from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from ArtHub.accounts.models import UserProfile, ArtHubUser
from ArtHub.accounts.views_mixins import DisabledFieldsFormMixin
from ArtHub.art.views_mixins import BootstrapFormMixin
UserModel = get_user_model()

class CreateRegularProfileForm(BootstrapFormMixin,UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    max_upload_limit = 5 * 1024 * 1024

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

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']
        if data > timezone.now().date():
            raise ValidationError("Date of birth cannot be a date in the future")
        elif data < date(1900, 1 , 1):
            raise ValidationError("Date of birth must be after 1 January 1900")
        return data

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserProfile.objects.filter(email=email).count() > 0:
            raise ValidationError('This email is already in use.')
        return email

    def save(self, commit=True):
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
        return user

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('profile_photo')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('profile_photo', f"File must be < 5 MB")


class RegularProfileUpdateForm(BootstrapFormMixin,forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
    max_upload_limit = 5 * 1024 * 1024

    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    profile_photo = forms.ImageField(

    )

    date_of_birth = forms.DateField(widget=forms.TextInput, disabled=True)
    email = forms.EmailField(

    )
    description = forms.TextInput(

    )

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('profile_photo')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('profile_photo', f"File must be < 5 MB")

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'profile_photo', 'date_of_birth', 'email', 'website','address','description']
        widgets = {

            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Add an address for visitors interested in your art'
                }
            ),
            'website': forms.TextInput(
                attrs={
                    'placeholder': 'Add a website'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Provide a general summary of your skills and your work'
                }
            ),

        }

class DeleteProfileForm(DisabledFieldsFormMixin, BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_disabled_fields()
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = ArtHubUser.objects.get(pk=self.instance.pk)
        own_art = user.art_piece__set
        own_art.delete()
        own_events = user.event_set
        own_events.delete()
        user.delete()
        self.instance.delete()
        return self.instance

    class Meta:
        model = UserProfile
        exclude = ('user', 'description', 'profile_photo', 'first_name', 'last_name', 'date_of_birth', 'email', )

