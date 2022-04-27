
from django.contrib.auth import mixins as auth_mixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from ArtHub.accounts.models import Artist
from django.views import generic as views

from ArtHub.art.forms import DeleteArtForm, CreateNewsForm, CreateEventForm
from ArtHub.art.models import ArtPiece, News, Event
from ArtHub.art.views_mixins import CheckArtModGroupMixin, CheckArtistOrAdModGroupMixin


class DashboardArtView(views.ListView):
    model = ArtPiece
    template_name = 'art/dashboard_art.html'
    context_object_name = 'art_objects'


class DashboardArtistsView(views.ListView):
    model = Artist
    template_name = 'art/dashboard_artists.html'
    context_object_name = 'artists_objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artists = Artist.objects.all()
        context['artists'] = artists
        return context

    ##maybe do this with def get_queryset ^^


class CreateArtView(CheckArtistOrAdModGroupMixin, auth_mixin.LoginRequiredMixin, views.CreateView):
    model = ArtPiece
    template_name = 'art/create_art.html'
    fields = ('title', 'photo', 'description', )

    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_name = 'add painting'
        context['url_name'] = url_name
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditArtView(CheckArtistOrAdModGroupMixin, auth_mixin.LoginRequiredMixin, views.UpdateView):
    model = ArtPiece
    template_name = 'art/edit_art.html'

    fields = '__all__'
    context_object_name = 'art_object'

    def get_success_url(self):
        painting_id = self.get_object().id
        return reverse_lazy('details art', kwargs={'pk': painting_id})

class ArtDetailsView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = ArtPiece
    template_name = 'art/details_art.html'
    context_object_name = 'art_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.object.user == self.request.user
        return context

class DeleteArtView(CheckArtistOrAdModGroupMixin, auth_mixin.LoginRequiredMixin,views.DeleteView):
    template_name = 'art/delete_art.html'
    form_class = DeleteArtForm
    queryset = ArtPiece.objects.all()
    # url = reverse_lazy('index')
    success_url = reverse_lazy('index')


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
    # model = News
    # fields = ('title', 'subtitle', 'content')
    form_class = CreateNewsForm
    success_url = reverse_lazy('dashboard news')
    permission_required = ('art.add_news', 'art.edit_news', 'art.delete_news')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DashboardNewsView(views.ListView):
    template_name = 'art/dashboard_news.html'
    model = News
    context_object_name = 'news'


class DetailsNewsView(views.DetailView):
    template_name = 'art/details_news.html'
    model = News
    context_object_name = 'news'


class UpdateNewsView(CheckArtModGroupMixin, LoginRequiredMixin, views.UpdateView):
    template_name = 'art/edit_news.html'
    model = News
    context_object_name = 'news'


class DeleteNewsView(CheckArtModGroupMixin, LoginRequiredMixin, views.DeleteView):
    template_name = 'art/delete_news.html'
    model = News
    context_object_name = 'news'


class CreateEventView(CheckArtistOrAdModGroupMixin, LoginRequiredMixin, views.CreateView):
    template_name = 'art/create_event.html'
    # model = Event
    # fields = ('title', 'description', 'location', 'date', 'price', )
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


class UpdateEventView(CheckArtistOrAdModGroupMixin, LoginRequiredMixin, views.UpdateView):
    template_name = 'art/edit_event.html'
    model = Event
    fields = ('title', 'description', 'location', 'date', 'price')
    context_object_name = 'event'
    success_url = reverse_lazy('dashboard events')

class DeleteEventView(CheckArtistOrAdModGroupMixin, LoginRequiredMixin, views.DeleteView):
    template_name = 'art/delete_event.html'
    model = Event
    context_object_name = 'event'




