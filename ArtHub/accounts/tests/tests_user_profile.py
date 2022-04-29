from unittest import TestCase

from django.urls import reverse

from ArtHub.accounts.models import UserProfile


class ProfileCreateViewTests(TestCase):
    VALID_PROFILE_DATA = {
        'first_name': 'Vera',
        'last_name': 'deRoos',
        'email': 'vera@abc.bg',
        'user': 8,
        'description': 'any description',
        'website': 'www.vera.com',
        'address': 'Ruse, Bulgaria'
    }

    def test_create_profile__when_all_valid__expect_to_create(self):
        self.client.post(
            reverse('create profile'),
            data=self.VALID_PROFILE_DATA,
        )

        profile = UserProfile.objects.first()
        self.assertIsNotNone(profile)
        self.assertEqual(self.VALID_PROFILE_DATA['first_name'], profile.first_name)
        self.assertEqual(self.VALID_PROFILE_DATA['last_name'], profile.last_name)
        self.assertEqual(self.VALID_PROFILE_DATA['email'], profile.email)
        self.assertEqual(self.VALID_PROFILE_DATA['user'], profile.user)
        self.assertEqual(self.VALID_PROFILE_DATA['description'], profile.description)
        self.assertEqual(self.VALID_PROFILE_DATA['website'], profile.website)
        self.assertEqual(self.VALID_PROFILE_DATA['address'], profile.address)

    def test_create_profile__when_all_valid__expect_to_redirect_to_details(self):
        response = self.client.post(
            reverse('create profile'),
            data=self.VALID_PROFILE_DATA,
        )

        profile = UserProfile.objects.first()

        expected_url = reverse('details profile', kwargs={'pk': profile.pk})
        self.assertRedirects(response, expected_url)



