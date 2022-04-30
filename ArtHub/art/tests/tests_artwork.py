from django.test import TestCase
from django.urls import reverse, reverse_lazy
from datetime import date

from django.test import RequestFactory


from ArtHub.accounts.models import UserProfile, Artist
from ArtHub.art.models import ArtPiece, Style, Technique, UserModel
from ArtHub.art.views.art import DashboardArtistsView


class ArtworkListViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345abcd',
        'type': 'ARTIST',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'profile_photo': 'http://test.picture/url.png',
        'date_of_birth': date(1990, 4, 13),
    }

    VALID_ART_DATA = {
        'title': 'The art',
        'type': 'painting',
        'medium_used': 'paint',
        'photo': 'asd.jpg',
        'publication_date': date.today(),
        'likes': 0,

    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = UserProfile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile)

    def test_get__expect_correct_template(self):
        response = self.client.get(reverse('dashboard art'))

        self.assertTemplateUsed(response, 'art/dashboard_art.html')

    def test_get__when_two_artpieces__expect_context_to_contain_two_artpieces(self):
        user, profile = self.__create_valid_user_and_profile()
        # style = Style(name='Baroque', description='Nice Style', photo='http://test.picture/url.png',)
        # style.save()
        # technique = Technique(name='AirBrush', description='Nice Technique', photo='http://test.picture/url.png',)
        # technique.save()

        art_to_create = (
            ArtPiece(
                title='Artsy',
                photo='http://test.picture/url.png',
                description='nice',
                publication_date=date(2020, 1, 1),
                medium_used='glass',
                likes=0,
                type='painting',
                user_id=1,
            ),
            ArtPiece(
                title='Artsy piece',
                photo='http://test.picture/url2.png',
                description='nicer',
                publication_date=date(2020, 1, 12),
                medium_used='bronze',
                likes=0,
                type='sculpture',
                user_id=1,
            ),
        )
        ArtPiece.objects.bulk_create(art_to_create)

        response = self.client.get(reverse_lazy('dashboard art'))

        art = response.context['object_list']
        self.assertEqual(len(art), 2)

class DashboardViewTests(TestCase):

    def test_if_correct_artists_queryset_returned(self):
        request = RequestFactory().get('/art')
        view = DashboardArtistsView()
        view.request = request

        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, Artist.objects.all())

