from django import forms
from django.contrib.auth.models import User

from control_panel.models import Member, Trainer, Product, Pass, Group


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
            user.set_password(new_password)
            user.save()
        return user


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


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_control_fields = ['name', 'validity', 'available_entries', 'activity', 'price']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Product
        fields = '__all__'


class PassForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_control_fields = ['product', 'status', 'start_date']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Pass
        exclude = ('member', 'end_date', 'entries')


class GroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_control_fields = ['name', 'level', 'program', 'trainer']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Group
        exclude = ('members', )


class GroupAddMembersForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('members', )
        widgets = {'members': forms.CheckboxSelectMultiple, }
