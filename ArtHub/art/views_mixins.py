from django.core.exceptions import PermissionDenied


class CheckArtModGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='ArtMod').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class CheckArtistOrAdModGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='ArtMod').exists() or request.user.groups.filter(name='Artist').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
