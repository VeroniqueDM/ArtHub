from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models
# Create your models here.
from ArtHub.accounts.managers import ArtHubManager
from ArtHub.common.validators import validate_only_letters, validate_file_max_size_in_mb


class ArtHubUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH = 25

    class Types(models.TextChoices):
        ARTIST = 'ARTIST'
        REGULAR_USER = 'REGULAR_USER'
        ART_MOD = 'ART_MOD'

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )
    type = models.CharField(
        max_length=50,
        choices=Types.choices,
        # default = Types.REGULAR_USER,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'
    objects = ArtHubManager()

    class Meta:
        app_label = 'accounts'
        # ordering = ('first_name','last_name')


class ArtistManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(ArtistManager, self).get_queryset(*args, **kwargs).filter(type=ArtHubUser.Types.ARTIST)


class RegularUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(RegularUserManager, self).get_queryset(*args, **kwargs).filter(type=ArtHubUser.Types.REGULAR_USER)


class ArtModManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(ArtModManager, self).get_queryset(*args, **kwargs).filter(type=ArtHubUser.Types.ART_MOD)


class Artist(ArtHubUser):
    objects = ArtistManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = ArtHubUser.Types.ARTIST


class RegularUser(ArtHubUser):
    objects = RegularUserManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = ArtHubUser.Types.REGULAR_USER


class ArtModUser(ArtHubUser):
    objects = ArtModManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = ArtHubUser.Types.ART_MOD


class UserProfile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    USER_TYPES = [(x, x) for x in ['Artist', 'Art-enthusiast']]
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    profile_photo = models.ImageField(
        blank=True,
        null=True,
        validators=(
            # validate_file_max_size_in_mb(5),
        )
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        ArtHubUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # is_artist = models.CharField(
    #     max_length=max(len(x) for x, _ in USER_TYPES),
    #
    #     default=False,
    #     choices=USER_TYPES,
    # )
    # styles = models.ManyToManyField(
    #     Style,
    # )
    description = models.TextField(

    )
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


