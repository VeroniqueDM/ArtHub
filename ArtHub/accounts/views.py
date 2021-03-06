from django.contrib.auth import mixins as auth_mixin, login, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth import logout as auth_logout
from django.urls import reverse_lazy, reverse
from django.contrib.auth import views as auth_views
from django.views import generic as views
from django.views.generic import RedirectView

from ArtHub.accounts.forms import CreateRegularProfileForm, RegularProfileUpdateForm
from ArtHub.accounts.models import UserProfile
from ArtHub.art.models import ArtPiece, Event

UserModel = get_user_model()


class RegularUserRegisterView(views.CreateView):
    form_class = CreateRegularProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('index')
    context_object_name = 'profile'

    def form_valid(self, form):
        result = super().form_valid(form)

        if self.object.type == 'ARTIST':
            group = Group.objects.get(name='Artist').id

            self.object.groups.add(group)
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserLogoutView(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(UserLogoutView, self).get(request, *args, **kwargs)


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'


class RegularProfileDetailsView(views.DetailView):
    model = UserProfile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own_art = ArtPiece.objects.filter(user_id=self.object.user)
        own_events = Event.objects.filter(user_id=self.object.user)
        total_likes_count = sum(pp.likes for pp in own_art)
        total_pieces_of_art = len(own_art)

        context.update({
            'total_likes_count': total_likes_count,
            'total_pieces_of_art': total_pieces_of_art,
            'is_owner': self.object.user_id == self.request.user.id,
            'own_art': own_art,
            'own_events': own_events,
        })

        return context


class EditRegularProfileView(auth_mixin.LoginRequiredMixin, views.UpdateView):
    template_name = 'accounts/profile_edit.html'
    context_object_name = 'profile'
    queryset = UserProfile.objects.all()
    form_class = RegularProfileUpdateForm

    def get_success_url(self):
        return reverse('details profile', kwargs={'pk': self.get_object().user_id})

    def get_context_data(self, **kwargs):
        context = super(EditRegularProfileView, self).get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(pk=self.get_object().user_id)
        context['profile_form'] = RegularProfileUpdateForm(
            instance=user_profile,
        )
        return context

    def form_valid(self, form):
        profile = form.save()
        user = profile.user
        user.last_name = form.cleaned_data['last_name']
        user.first_name = form.cleaned_data['first_name']
        user.profile_photo = form.cleaned_data['profile_photo']
        user.date_of_birth = form.cleaned_data['date_of_birth']
        user.email = form.cleaned_data['email']
        user.website = form.cleaned_data['website']
        user.address = form.cleaned_data['address']
        user.description = form.cleaned_data['description']
        user.save()
        return super(EditRegularProfileView, self).form_valid(form)

    def get_queryset(self):
        if self.request.user.type == 'ARTIST':
            return UserModel.objects.filter(id=self.request.user.id)

class DeleteProfileView(views.DeleteView):
    template_name = 'accounts/profile_delete.html'
    model = UserModel
    success_url = reverse_lazy('index')

    def get_queryset(self):
        if self.request.user.type == 'ARTIST':
            return UserModel.objects.filter(id=self.request.user.id)
