from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin

from ArtHub.art.models import News, UserNewsTimestamp

from django.views import generic as views
from django.utils.timezone import now


