from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from ArtHub.art.forms import CreateStyleForm, CreateTechniqueForm, EditStyleForm, EditTechniqueForm
from ArtHub.art.models import Style, Technique
from ArtHub.art.views_mixins import CheckArtModGroupMixin

from django.views import generic as views


class CreateStyleView(CheckArtModGroupMixin, LoginRequiredMixin, views.CreateView):
    template_name = 'art/create_style.html'
    form_class = CreateStyleForm
    success_url = reverse_lazy('dashboard styles')


class DashboardStylesView(CheckArtModGroupMixin,  LoginRequiredMixin, views.ListView):
    template_name = 'art/dashboard_styles.html'
    model = Style
    context_object_name = 'styles'


class DetailsStyleView(views.DetailView):
    template_name = 'art/details_style.html'
    model = Style
    context_object_name = 'style'


class UpdateStyleView(CheckArtModGroupMixin, LoginRequiredMixin, views.UpdateView):
    template_name = 'art/edit_style.html'
    form_class = EditStyleForm
    queryset = Style.objects.all()
    context_object_name = 'style'
    success_url = reverse_lazy('dashboard styles')


class DeleteStyleView(CheckArtModGroupMixin, LoginRequiredMixin, views.DeleteView):
    template_name = 'art/delete_style.html'
    model = Style
    fields = ()
    context_object_name = 'style'
    success_url = reverse_lazy('dashboard styles')


class CreateTechniqueView(CheckArtModGroupMixin, LoginRequiredMixin, views.CreateView):
    template_name = 'art/create_technique.html'
    form_class = CreateTechniqueForm
    success_url = reverse_lazy('dashboard techniques')


class DashboardTechniqueView(CheckArtModGroupMixin, LoginRequiredMixin,views.ListView):
    template_name = 'art/dashboard_techniques.html'
    model = Technique
    context_object_name = 'techniques'


class DetailsTechniqueView(views.DetailView):
    template_name = 'art/details_technique.html'
    model = Technique
    context_object_name = 'technique'


class UpdateTechniqueView(CheckArtModGroupMixin, LoginRequiredMixin, views.UpdateView):
    template_name = 'art/edit_technique.html'
    form_class = EditTechniqueForm
    queryset = Technique.objects.all()
    success_url = reverse_lazy('dashboard techniques')
    context_object_name = 'technique'


class DeleteTechniqueView(CheckArtModGroupMixin, LoginRequiredMixin, views.DeleteView):
    template_name = 'art/delete_technique.html'
    model = Technique
    fields = ()
    context_object_name = 'technique'
    success_url = reverse_lazy('dashboard techniques')


