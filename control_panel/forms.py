from django import forms

from django.contrib.auth.models import User

from control_panel.models import Member, Trainer


class LoginForm(forms.Form):

    email = forms.EmailField(label='')
    email.widget.attrs.update({'class': 'form-control', 'placeholder': 'Email', 'required': True, 'autofocus': True})

    password = forms.CharField(label='', widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'form-control', 'placeholder': 'Password', 'required': True})


class EditUserForm(forms.ModelForm):

    password = forms.CharField(label='Hasło', widget=forms.PasswordInput, required=False)
    password_confirmation = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_control_fields = ['first_name', 'last_name', 'email', 'password', 'password_confirmation']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = ('first_name', 'last_name', 'email')
        model = User
        
    def clean(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)

        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']

        if password != password_confirmation:
            self.add_error('password_confirmation', 'Hasła się nie zgadzają')

    def save(self, commit=True):
        user = super().save(commit=commit)
        new_password = self.cleaned_data['password']
        if new_password:
            user.set_password()
            user.save()


class MemberForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_control_fields = ['first_name', 'last_name', 'phone', 'mail', 'status', 'description']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.fields['description'].widget.attrs.update({'rows': '4'})
        self.fields['description'].required = False

    class Meta:
        model = Member
        fields = '__all__'


class TrainerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_control_fields = ['first_name', 'last_name', 'phone', 'mail']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
        self.fields['mail'].required = False

    class Meta:
        model = Trainer
        fields = '__all__'

