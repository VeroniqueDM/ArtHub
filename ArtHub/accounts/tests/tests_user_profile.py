from unittest import TestCase

from django.core.exceptions import ValidationError
from django.urls import reverse

from ArtHub.accounts.models import UserProfile
from ArtHub.art.models import ArtPiece
from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

UserModel = get_user_model()


class ProfileDetailsViewTests(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345abcd',
        'type': 'ARTIST',
        # 'id': 1,
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'profile_photo': 'http://test.picture/url.png',
        'date_of_birth': date(1990, 4, 13),
        'user_id' : 1,
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

    def __create_art_for_user(self, user):
        art = ArtPiece.objects.create(
            **self.VALID_ART_DATA,
            user=user,
        )

        return art

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('details profile', kwargs={'pk': profile.pk}))

    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('details profile', kwargs={
            'pk': 1,
        }))

        self.assertEqual(404, response.status_code)

    def test_expect_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile(profile)
        self.assertTemplateUsed('accounts/profile_details.html')

    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.__get_response_for_profile(profile)

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser23',
            'password': '12345qwe',
            'type' : 'ARTMOD'
        }

        self.__create_user(**credentials)

        self.client.login(**credentials)

        response = self.__get_response_for_profile(profile)

        self.assertFalse(response.context['is_owner'])

    def test_when_no_art_likes__expect_total_likes_count_to_be_zero(self):
        user, profile = self.__create_valid_user_and_profile()
        self.__create_art_for_user(user)
        response = self.__get_response_for_profile(profile)

        self.assertEqual(0, response.context['own_art'][0].likes)

    def test_when_photo_likes__expect_total_likes_count_to_be_correct(self):
        likes = 3
        user, profile = self.__create_valid_user_and_profile()
        art = self.__create_art_for_user(user)
        art.likes = likes
        art.save()

        response = self.__get_response_for_profile(profile)

        self.assertEqual(likes, response.context['own_art'][0].likes)

    def test_when_no_photos__no_photos_count(self):
        # same as likes
        pass

    def test_when_user_has_art__expect_to_return_only_users_art(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '12345qwe',
            'type': 'ARTIST'
        }
        user2 = self.__create_user(**credentials)

        art = self.__create_art_for_user(user)
        self.__create_art_for_user(user2)

        response = self.__get_response_for_profile(profile)

        self.assertQuerysetEqual(
            [art],
            response.context['own_art'],
        )

    def test_when_user_has_art__art_should_be_empty(self):
        _, profile = self.__create_valid_user_and_profile()

        response = self.__get_response_for_profile(profile)
        self.assertQuerysetEqual(
            [],
            response.context['own_art'],
        )

    def test_when_no_pets__likes_and_photos_count_should_be_0(self):
        pass

#
# class ProfileTests(TestCase):
#     VALID_USER_CREDENTIALS = {
#         'username': 'testuser',
#         'password': '12345abcd',
#         'type': 'ARTIST'
#     }
#
#     VALID_PROFILE_DATA = {
#         'first_name': 'Test',
#         'last_name': 'User',
#         'profile_photo': 'http://test.picture/url.png',
#         'date_of_birth': date(1990, 4, 13),
#     }

    def test_user_and_profile_create__when_first_name_contains_only_letters__expect_success(self):
        # profile = UserProfile(**self.VALID_PROFILE_DATA)
        # profile.save()
        # self.assertIsNotNone(profile.pk)
        new_user = UserModel.objects.create_user(
            username='testuser',
            # password='12345abcd',
            type='ARTIST',)
        self.assertEqual(new_user.username, "testuser")
        self.assertEqual(new_user.type, "ARTIST")
        self.assertIs(new_user.is_staff, False)
        profile = UserProfile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=new_user,
        )
        profile.save()
        self.assertIsNotNone(profile.pk)
        # self.assertEqual(
        #     new_user., "New_user Profile")

    def test_profile_create__when_first_name_contains_a_digit__expect_to_fail(self):
        first_name = 'Doncho1'
        profile = UserProfile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],

            profile_photo= 'http://test.picture/url.png',
            date_of_birth=date(1990, 4, 13),
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_percentage_sign__expect_to_fail(self):
        first_name = 'Ver&%a'
        profile = UserProfile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],

            profile_photo='http://test.picture/url.png',
            date_of_birth=date(1990, 4, 13),
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_to_fail(self):
        first_name = 'Ver ito'
        profile = UserProfile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],

            profile_photo='http://test.picture/url.png',
            date_of_birth=date(1990, 4, 13),
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)


