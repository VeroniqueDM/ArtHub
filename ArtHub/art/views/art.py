from django.contrib.auth import mixins as auth_mixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import now

from ArtHub.accounts.models import UserProfile
from django.views import generic as views

from ArtHub.art.forms import DeleteArtForm, CreateNewsForm, CreateEventForm, CreateArtForm, EditEventForm, EditNewsForm, \
    EditArtForm
from ArtHub.art.models import ArtPiece, News, Event, UserNewsTimestamp
from ArtHub.art.views_mixins import CheckArtModGroupMixin, CheckArtistOrAdModGroupMixin


class DashboardArtView(views.ListView):
    model = ArtPiece
    template_name = 'art/dashboard_art.html'
    context_object_name = 'art_objects'


class DashboardArtistsView(views.ListView):
    model = UserProfile
    template_name = 'art/dashboard_artists.html'
    context_object_name = 'artists'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__type='ARTIST')


class CreateArtView(CheckArtistOrAdModGroupMixin, auth_mixin.LoginRequiredMixin, views.CreateView):
    template_name = 'art/create_art.html'
    form_class = CreateArtForm

    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditArtView(CheckArtistOrAdModGroupMixin, auth_mixin.LoginRequiredMixin, views.UpdateView):
    template_name = 'art/edit_art.html'
    form_class = EditArtForm
    queryset = ArtPiece.objects.all()
    context_object_name = 'art_object'

    def get_queryset(self):
        return ArtPiece.objects.filter(user_id=self.request.user)

    def get_success_url(self):
        painting_id = self.get_object().id
        return reverse_lazy('details art', kwargs={'pk': painting_id})


class ArtDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = ArtPiece
    template_name = 'art/details_art.html'
    context_object_name = 'art_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        styles=self.object.style.all()
        techniques=self.object.technique.all()
        context['is_owner'] = self.object.user == self.request.user
        context['styles'] = styles
        context['owner'] = UserProfile.objects.get(user_id=self.object.user)
        context['techniques'] = techniques
        return context


class DeleteArtView(auth_mixin.LoginRequiredMixin,views.DeleteView):
    template_name = 'art/delete_art.html'
    form_class = DeleteArtForm
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return ArtPiece.objects.filter(user_id=self.request.user)




@login_required
def like_art(request, pk):
    art = ArtPiece.objects.get(pk=pk)
    current_user_liked = art.liked_by.filter(id=request.user.id)
    if not current_user_liked:
        art.liked_by.add(request.user)
        art.likes += 1
        art.save()

    return redirect('details art', pk)


class CreateNewsView(CheckArtModGroupMixin, LoginRequiredMixin, views.CreateView):
    template_name = 'art/create_news.html'
    form_class = CreateNewsForm
    success_url = reverse_lazy('dashboard news')
    # COULD BE REMOVED
    permission_required = ('art.add_news', 'art.edit_news', 'art.delete_news')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DashboardNewsView(views.ListView):
    template_name = 'art/dashboard_news.html'
    model = News
    context_object_name = 'news'


class NewsListLastSeenView(LoginRequiredMixin,views.ListView):
    model = News
    template_name = "art/last_seen_news.html"
    context_object_name = "last_seen_news"
    queryset = News.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        # ALTERNATIVELY, THIS FIRST SORTS THE NEWS SEEN BEFORE, THEN SHOWS ALL ELSE
        # if user.is_authenticated:
        #     queryset_one = queryset.filter(
        #         timestamps__user=user).order_by("-timestamps__timestamp")
        #     queryset_two = queryset.exclude(timestamps__user=self.request.user)
        #     queryset = chain(queryset_one, queryset_two)
        queryset_one = queryset.filter(
            timestamps__user=user).order_by("-timestamps__timestamp")
        return queryset_one


class DetailsNewsView(LoginRequiredMixin, views.DetailView):
    model = News
    template_name = "art/details_news.html"
    context_object_name = 'news'

    def get(self, request, *args, **kwargs):
        self.user_viewed(now())
        return super().get(request, *args, **kwargs)

    def user_viewed(self, timestamp):
        user = self.request.user
        if not user.is_authenticated:
            return
        upt, _ = UserNewsTimestamp.objects.get_or_create(
            user=user, news=self.get_object())
        upt.timestamp = timestamp
        upt.save()
        return upt.timestamp

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timestamper = UserNewsTimestamp.objects.get(user_id=self.request.user.id, news_id=self.object)
        timestamp = timestamper.timestamp
        context['timestamp'] = timestamp
        return context

class UpdateNewsView(CheckArtModGroupMixin, LoginRequiredMixin, views.UpdateView):
    template_name = 'art/edit_news.html'
    form_class = EditNewsForm
    queryset = News.objects.all()
    context_object_name = 'news'


class DeleteNewsView(CheckArtModGroupMixin, LoginRequiredMixin, views.DeleteView):
    template_name = 'art/delete_news.html'
    model = News
    context_object_name = 'news'


class CreateEventView(CheckArtistOrAdModGroupMixin, LoginRequiredMixin, views.CreateView):
    template_name = 'art/create_event.html'
    form_class = CreateEventForm
    success_url = reverse_lazy('dashboard events')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DashboardEventView(views.ListView):
    template_name = 'art/dashboard_event.html'
    model = Event
    context_object_name = 'events'


class DetailsEventView(views.DetailView):
    template_name = 'art/details_event.html'
    model = Event
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context

class UpdateEventView(CheckArtistOrAdModGroupMixin, LoginRequiredMixin, views.UpdateView):
    template_name = 'art/edit_event.html'
    form_class = EditEventForm
    queryset = Event.objects.all()
    context_object_name = 'event'
    success_url = reverse_lazy('dashboard events')

    def get_queryset(self):
        if self.request.user.type == 'ARTIST':
            return Event.objects.filter(user_id=self.request.user.id)

class DeleteEventView(CheckArtistOrAdModGroupMixin, LoginRequiredMixin, views.DeleteView):
    template_name = 'art/delete_event.html'
    model = Event
    context_object_name = 'event'

    def get_queryset(self):
        if self.request.user.type == 'ARTIST':
            return Event.objects.filter(user_id=self.request.user.id)



