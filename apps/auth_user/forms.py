from django.contrib.auth.forms import UserCreationForm

from apps.auth_user.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'phone_number')


class CustomUniversalFormForUser(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)
