from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import User, ForgotPassword


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(widget=forms.TextInput(attrs={'required':'True'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'required':'True'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

    def clean_email(self):
	    data = self.cleaned_data['email']
	    if User.objects.filter(email=data).exists():
	        raise forms.ValidationError("This email is already used")
	    return data   

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
	        raise forms.ValidationError("This username is already used")
        return data 


class ForgotPasswordForm(forms.Form):

    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.site = kwargs.pop('site', None)
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if not qs.exists():
            raise forms.ValidationError("Account does not exist for this email")
        return email


class ResetPasswordForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(), min_length=7)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=7)

    class Meta:
        model = User
        fields = [
            'password',
            'confirm_password',
        ]

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            error = 'Passwords do not match'
            self.add_error('password', error)
        return password

    def save(self, commit=True):
        user = super(ResetPasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["confirm_password"])
        if commit:
            user.save()
        return user