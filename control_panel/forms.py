from django import forms
from django.contrib.auth.models import User

from control_panel.models import Activity, Group, Member, Product, Pass, Trainer


class LoginForm(forms.Form):
    email = forms.EmailField(label='')
    password = forms.CharField(label='', widget=forms.PasswordInput)

    email.widget.attrs.update({'class': 'form-control',
                               'placeholder': 'Email',
                               'required': True,
                               'autofocus': True})
    password.widget.attrs.update({'class': 'form-control',
                                  'placeholder': 'Password',
                                  'required': True})


class MemberForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['first_name', 'last_name', 'birth_date', 'gender', 'phone', 'mail', 'status', 'notes']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.fields['notes'].widget.attrs.update({'rows': '4'})
        self.fields['birth_date'].widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = Member
        exclude = ('img',)


class TrainerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['first_name', 'last_name', 'birth_date', 'gender', 'phone', 'mail', 'status', 'notes',
                           'hourly_rate', 'employment_type']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.fields['notes'].widget.attrs.update({'rows': '4'})
        self.fields['birth_date'].widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = Trainer
        exclude = ('img',)


class GroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['color', 'max_capacity', 'activity', 'trainer', 'days', 'class_time', 'level']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.fields['days'].widget.attrs.update({'size': 8})

    class Meta:
        model = Group
        exclude = ('members',)


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['type', 'activity', 'partner_name', 'validity', 'available_entries', 'price', 'deposit',
                           'entry_surcharge', 'absence_surcharge']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Product
        fields = '__all__'


class ActivityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': '4', 'class': 'form-control'})

    class Meta:
        model = Activity
        fields = '__all__'


class PassForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_control_fields = ['product', 'start_date', 'end_date', 'paid']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Pass
        exclude = ('member', 'entries')


class GroupAddMembersForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('members',)
        widgets = {'members': forms.CheckboxSelectMultiple, }


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
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Adres e-mail',
        }

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


class UpdatePassForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_control_fields = ['start_date', 'end_date']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Pass
        fields = ('start_date', 'end_date')
