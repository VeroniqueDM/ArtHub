from itertools import chain
from operator import attrgetter

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from django.views import generic as views

from ArtHub.art.models import ArtPiece, News

UserModel = get_user_model()

class HomeView(ListView):
    template_name = 'home_page.html'
    # model = Painting
    def get_queryset(self):
        queryset = ArtPiece.objects.order_by('likes')
        # qs1 = Painting.objects.all()  # your first qs
        # qs2 = Sculpture.objects.all()  # your second qs
        # qs3 = OtherArt.objects.all()  # your second qs
        # queryset = sorted(chain(qs1, qs2, qs3), key=attrgetter('likes'))[:6]
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art = ArtPiece.objects.order_by('-likes')[:3]
        news = News.objects.order_by('-creation_date')[:3]
        context['art'] = art
        context['news'] = news
        return context

class LikedArtView(LoginRequiredMixin, ListView):
    template_name = 'art/dashboard_liked_art.html'

    def get_queryset(self):
        queryset = ArtPiece.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked_art = UserModel.objects.get(pk=self.request.user.pk).liked_by.all()
        context['liked_art'] = liked_art
        return context


