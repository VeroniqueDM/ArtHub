from django.contrib.auth.models import PermissionsMixin
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


class BootstrapFormMixin:
    fields = {}

    def _init_bootstrap_form_controls(self):
        for _, field in self.fields.items():
            # if field == 'medium_used':
            #     continue
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += 'form-control'
