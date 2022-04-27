from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from ArtHub.accounts.views import UserLoginView, RegularUserRegisterView, RegularProfileDetailsView, \
    ChangeUserPasswordView, \
    UserLogoutView, EditRegularProfileView, DeleteProfileView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('register/', RegularUserRegisterView.as_view(), name='register'),
    path('<int:pk>/', RegularProfileDetailsView.as_view(), name='details profile'),
    path('profile/edit/<int:pk>/', EditRegularProfileView.as_view(), name='edit profile'),
    path('profile/delete/<int:pk>/', DeleteProfileView.as_view(), name='delete profile'),
    path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('dashboard')), name='password_change_done'),
]