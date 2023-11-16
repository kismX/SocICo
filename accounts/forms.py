from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('name', )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
<<<<<<< Updated upstream
        fields = UserChangeForm.Meta.fields

=======
        fields = UserChangeForm.Meta.fields
>>>>>>> Stashed changes
