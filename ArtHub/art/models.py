from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
# from ArtHub.common.validators import validate_file_max_size_in_mb
# from ArtHub.accounts.models import ArtHubUser
UserModel = get_user_model()


class Style(models.Model):
    name = models.CharField(
        max_length=50,

    )
    description = models.TextField()
    photo = models.ImageField(
        null=True,
        blank=True,
        validators=(
            # validate_file_max_size_in_mb(5),
        ),
    )

    def __str__(self):
        return self.name


class Technique(models.Model):
    name = models.CharField(
        max_length=50,

    )
    description = models.TextField()
    photo = models.ImageField(
        null=True,
        blank=True,
        validators=(
            # validate_file_max_size_in_mb(5),
        ),
    )

    def __str__(self):
        return self.name

class ArtPiece(models.Model):
    MAX_LENGTH_TITLE = 50
    STYLES = ['Modernism', 'Impressionism', 'Abstract Art', 'Expressionism', 'Cubism', 'Surrealism',]
    CHOICES_STYLES = [(x, x) for x in STYLES]
    MEDIUMS = ['painting', 'drawing', 'print',]
    CHOICES_MEDIUM = [(x, x) for x in MEDIUMS]
    title = models.CharField(
        max_length= MAX_LENGTH_TITLE,
    )

    photo = models.ImageField(
        null=True,
        blank=True,
        validators=(
            # validate_file_max_size_in_mb(5),

        )
    )
    description = models.TextField(
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    style = models.ManyToManyField(
        Style,
        blank=True,
        null=True,
    )
    technique = models.ManyToManyField(
        Technique,
        blank=True,
        null=True,
    )

    medium_used = models.CharField(
        blank=True,
        null=True,
        max_length=max(len(x) for (x, _) in CHOICES_MEDIUM),
        choices=CHOICES_MEDIUM,
    )
    # is_framed = models.BooleanField(
    #     default=False,
    # )
    likes = models.IntegerField(
        default=0,
    )
    liked_by = models.ManyToManyField(
        UserModel,
        related_name= 'likes',
    )


class Event(models.Model):
    LOCATION_MAX_LEN = 100
    MAX_LENGTH_TITLE = 50
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    location = models.CharField(
        max_length=LOCATION_MAX_LEN,
    )
    date = models.DateField(

    )

    price = models.FloatField(
        validators=(

        )
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    photo = models.URLField(
        verbose_name = 'Photo URL'
    )

class News(models.Model):
    title = models.CharField(
        max_length=200,
    )
    subtitle = models.TextField(
        max_length=400,
    )
    creation_date = models.DateField(
        auto_now_add=True,
    )
    content = models.TextField(

    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    photo = models.URLField(
        verbose_name='Photo URL'

    )
