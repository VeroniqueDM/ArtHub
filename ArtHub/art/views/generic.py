from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


from ArtHub.art.models import ArtPiece, News

UserModel = get_user_model()


class HomeView(ListView):
    template_name = 'home_page.html'

    def get_queryset(self):
        queryset = ArtPiece.objects.order_by('likes')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art = ArtPiece.objects.order_by('-likes')[:5]
        news = News.objects.order_by('-creation_date')[:5]
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


