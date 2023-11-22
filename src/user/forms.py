from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django import forms


User = get_user_model()
class AdminChangeForm(forms.ModelForm):
    # pass
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'

    def clean_data(self):
        return self.initial['password']