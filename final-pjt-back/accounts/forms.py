from django import forms
from django.contrib.auth import get_user_model


# profile image 파일을 담기 위한 form
class UserForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ('profile_image',)