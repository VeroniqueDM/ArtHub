from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from cloudinary.models import CloudinaryField

UserModel = get_user_model()


class Style(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,

    )
    description = models.TextField()
    # photo = models.ImageField(
    #     null=True,
    #     blank=True,
    #     validators=(
    #
    #     ),
    # )
    photo = CloudinaryField(
        # upload_to='profile_photos/',
        'image',
        #     blank=True,
        #     null=True,
    )
    def __str__(self):
        return self.name


class Technique(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,

    )
    description = models.TextField()
    # photo = models.ImageField(
    #     null=True,
    #     blank=True,
    #     validators=(
    #
    #     ),
    # )
    photo = CloudinaryField(
        # upload_to='profile_photos/',
        'image',
        #     blank=True,
        #     null=True,
    )
    def __str__(self):
        return self.name


class ArtPiece(models.Model):
    MAX_LENGTH_TITLE = 50
    title = models.CharField(
        max_length= MAX_LENGTH_TITLE,
    )

    # photo = models.ImageField(
    #     null=True,
    #     blank=True,
    #     validators=(
    #
    #     )
    # )
    photo = CloudinaryField(
        # upload_to='profile_photos/',
     'image',
    #     blank=True,
    #     null=True,
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
        max_length = 200,
    )

    likes = models.IntegerField(
        default=0,
    )
    liked_by = models.ManyToManyField(
        UserModel,
        related_name= 'liked_by',
    )
    type = models.CharField(
        max_length=60,
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
            MinValueValidator(0),
        )
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    # photo = models.URLField(
    #     verbose_name = 'Photo URL'
    # )
    photo = CloudinaryField(
        # upload_to='profile_photos/',
        'image',
        #     blank=True,
        #     null=True,
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
    # update_date = models.DateField(
    #     auto_now=True,
    # )
    content = models.TextField(

    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    # photo = models.URLField(
    #     verbose_name='Photo URL'
    #
    # )
    photo = CloudinaryField(
        # upload_to='profile_photos/',
        'image',
        #     blank=True,
        #     null=True,
    )


class UserNewsTimestamp(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="timestamps")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="timestamps")
    timestamp = models.DateTimeField("Time Stamp", blank=True, null=True)
