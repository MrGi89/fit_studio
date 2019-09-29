from django import forms
from django.contrib.auth.models import User

from control_panel.models import Activity, Group, Member, Product, Pass, Trainer, Studio


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

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
        self.fields['birth_date'].widget.attrs.update({'autocomplete': 'off', 'id': 'trainer_id'})

    class Meta:
        model = Trainer
        exclude = ('img',)


class GroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['color', 'max_capacity', 'activity', 'days', 'trainer', 'class_time', 'level']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        self.fields['days'].widget.attrs.update({'size': 7})

    class Meta:
        model = Group
        exclude = ('members',)


class GroupMemberForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['members'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Group
        fields = ('members',)


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

        form_control_fields = ['product', 'start_date', 'end_date']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        for product in self.fields['product'].choices.queryset:
            self.fields['product'].widget.attrs.update({'data-product-{}'.format(product.id): product.price})

    class Meta:
        model = Pass
        exclude = ('entries',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_control_fields = ['first_name', 'last_name', 'email', 'password', 'password_confirmation']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean(self):

        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']

        if password != password_confirmation:
            self.add_error('password_confirmation', 'Passwords do not match.')

    def save(self, commit=True):
        user = super().save(commit=commit)
        new_password = self.cleaned_data['password']
        if new_password:
            user.set_password(new_password)
            user.save()
        return user


class StudioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['name', 'company_name', 'street', 'postal_code', 'city', 'nip', 'regon', 'mail', 'phone']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Studio
        fields = '__all__'


class GroupAddMembersForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('members',)
        widgets = {'members': forms.CheckboxSelectMultiple, }


class UpdatePassForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        form_control_fields = ['start_date', 'end_date']
        for field_name in form_control_fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Pass
        fields = ('start_date', 'end_date')
