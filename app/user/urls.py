"""
URL mappings for the user api
"""

from django.urls import path
from user import views

# reverse function looks for this app_name:Name of the view defined in the urlpatterns
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/',views.CreateTokenView.as_view(), name='token'),
    path('me/',views.ManageUserView.as_view(), name="me")
]

