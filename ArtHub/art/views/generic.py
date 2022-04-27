from itertools import chain
from operator import attrgetter

from django.views.generic import ListView

from ArtHub.accounts.views_mixins import RedirectToDashboard
from django.views import generic as views

from ArtHub.art.models import ArtPiece


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
    #     qs1 = Painting.objects.all()  # your first qs
    #     qs2 = Sculpture.objects.all()  # your second qs
    #     qs3 = OtherArt.objects.all()  # your second qs
    #     # you can add as many qs as you want
    #     top_liked_art = sorted(chain(qs1, qs2, qs3), key=attrgetter('likes'))[:6]
    #     context['hide_additional_nav_items'] = True
    #     # FILTERED TOP 6 ART ITEMS
    #
        context['art'] = art
        return context

