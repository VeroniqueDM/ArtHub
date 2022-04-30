from django.urls import path

from ArtHub.art.views.art import DashboardArtView, CreateArtView, ArtDetailsView, EditArtView, DeleteArtView, \
    DashboardEventView, CreateEventView, DetailsEventView, UpdateEventView, DeleteEventView, DashboardNewsView, \
    CreateNewsView, DetailsNewsView, UpdateNewsView, DeleteNewsView, DashboardArtistsView, like_art, \
    NewsListLastSeenView
from ArtHub.art.views.generic import HomeView, LikedArtView
from ArtHub.art.views.styles_and_techniques import DashboardStylesView, CreateStyleView, DetailsStyleView, \
    UpdateStyleView, DeleteStyleView, DashboardTechniqueView, CreateTechniqueView, DetailsTechniqueView, \
    UpdateTechniqueView, DeleteTechniqueView


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('dashboard/art/', DashboardArtView.as_view(), name='dashboard art'),
    path('art/add/', CreateArtView.as_view(), name='add art'),
    path('art/details/<int:pk>/', ArtDetailsView.as_view(), name='details art'),
    path('art/edit/<int:pk>/', EditArtView.as_view(), name='edit art'),
    path('art/delete/<int:pk>/', DeleteArtView.as_view(), name='delete art'),
    path('art/favourites/', LikedArtView.as_view(), name='liked art'),
    path('art/like/<int:pk>/', like_art, name='like art'),

    path('events/dashboard/', DashboardEventView.as_view(), name='dashboard events'),
    path('events/add/', CreateEventView.as_view(), name='add event'),
    path('events/details/<int:pk>/', DetailsEventView.as_view(), name='details event'),
    path('events/edit/<int:pk>/', UpdateEventView.as_view(), name='edit event'),
    path('events/delete/<int:pk>/', DeleteEventView.as_view(), name='delete event'),

    path('news/dashboard/', DashboardNewsView.as_view(), name='dashboard news'),
    path('news/add/', CreateNewsView.as_view(), name='add news'),
    path('news/details/<int:pk>/', DetailsNewsView.as_view(), name='details news'),
    path('news/edit/<int:pk>/', UpdateNewsView.as_view(), name='edit news'),
    path('news/delete/<int:pk>/', DeleteNewsView.as_view(), name='delete news'),
    path('news/last-viewed/', NewsListLastSeenView.as_view(), name='last seen news'),

    path('styles/dashboard/', DashboardStylesView.as_view(), name='dashboard styles'),
    path('styles/add/', CreateStyleView.as_view(), name='add style'),
    path('styles/details/<int:pk>/', DetailsStyleView.as_view(), name='details style'),
    path('styles/edit/<int:pk>/', UpdateStyleView.as_view(), name='edit style'),
    path('styles/delete/<int:pk>/', DeleteStyleView.as_view(), name='delete style'),

    path('techniques/dashboard/', DashboardTechniqueView.as_view(), name='dashboard techniques'),
    path('techniques/add/', CreateTechniqueView.as_view(), name='add technique'),
    path('techniques/details/<int:pk>/', DetailsTechniqueView.as_view(), name='details technique'),
    path('techniques/edit/<int:pk>/', UpdateTechniqueView.as_view(), name='edit technique'),
    path('techniques/delete/<int:pk>/', DeleteTechniqueView.as_view(), name='delete technique'),

    path('artists/dashboard/', DashboardArtistsView.as_view(), name='dashboard artists'),


]
