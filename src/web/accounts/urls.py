from django.urls import path, include
from .views import LogoutView, CrossAuthView, UserUpdateView, IdentificationCheck, ProfileCompleteView

app_name = 'users'
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/change/', UserUpdateView.as_view(), name='user-change'),
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth'),

    path('identification/', IdentificationCheck.as_view(), name='identification-check'),
    path('agency/profile/', ProfileCompleteView.as_view(), name='agency-profile-complete'),


]


