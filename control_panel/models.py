import googlemaps

from datetime import date, datetime, timedelta
from django.db import models
from control_panel.widgets import ColorWidget
from django.conf import settings

GENDER_CHOICES = ((1, 'Kobieta'), (2, 'Mężczyzna'))
STATUS_CHOICES = ((1, 'Aktywny'), (2, 'Nieaktywny'))
EMPLOYMENT_CHOICES = ((1, 'UoP'), (2, 'UoZ'), (3, 'UoD'), (4, 'B2B'))
LEVEL_CHOICES = ((1, 'Podstawowa'), (2, 'Średnio-zaawansowana'), (3, 'Zaawansowana'))
PRODUCT_CHOICES = ((1, 'Karnet'), (2, 'Karta'), (3, 'Wejściówka'))
PARTNER_CHOICES = ((1, 'Multisport'), (2, 'Fit-Profit'), (3, 'OK System'))
ACTIVITY_CHOICES = ((1, 'Pole Dance'), (2, 'Exotic'), (3, 'Stretching'), (4, 'Jumping'))
COLOR_CHOICES = ((1, 'green'), (2, 'red'), (3, 'black'), (4, 'yellow'), (5, 'blue'))


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)


class Member(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, default=1)
    phone = models.IntegerField()
    mail = models.EmailField(unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    notes = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='user_img/', default='user_img/default.jpg')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.last_name.capitalize() + ' ' + self.first_name.capitalize()


class Trainer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, default=1)
    phone = models.IntegerField()
    mail = models.EmailField(unique=True, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    notes = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='trainer_img/', default='trainer_img/default.jpg')
    hourly_rate = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    employment_type = models.PositiveSmallIntegerField(choices=EMPLOYMENT_CHOICES, default=1)

    def __str__(self):
        return '{} {}'.format(self.last_name.capitalize(), self.first_name.capitalize())


class Product(models.Model):
    type = models.PositiveSmallIntegerField(choices=PRODUCT_CHOICES)
    activity = models.ForeignKey('Activity', models.CASCADE, related_name='products')
    partner_name = models.PositiveSmallIntegerField(choices=PARTNER_CHOICES, blank=True, null=True)
    validity = models.PositiveSmallIntegerField(blank=True, null=True)
    available_entries = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    entry_surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    absence_surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):

        if self.type == 2:
            return '{} {} {}'.format(self.get_type_display(), self.get_partner_name_display(), self.activity.name)
        else:
            return '{} {}'.format(self.get_type_display(), self.activity.name)


class Activity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):

    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=1)
    color = ColorField(unique=True)
    max_capacity = models.IntegerField()
    activity = models.ForeignKey(Activity, models.CASCADE, related_name='groups')
    trainer = models.ForeignKey(Trainer, models.SET_NULL, null=True, related_name='groups')
    members = models.ManyToManyField(Member)
    days = models.ManyToManyField('Day')
    class_time = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        days = ' - '.join([day.name[:3] for day in self.days.all()])
        return '{} {:%H:%M} {}'.format(days, self.class_time, self.activity.name)


class Pass(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='passes')
    product = models.ForeignKey(Product, on_delete=None, related_name='products')
    paid = models.BooleanField(default=0)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return '{} {} - {}'.format(self.product, self.member, self.paid)


class Entry(models.Model):
    current_pass = models.ForeignKey(Pass, on_delete=models.CASCADE, related_name='entries')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{:%Y-%m-%d %H:%M}'.format(self.created)


class Payment(models.Model):
    date = models.DateField()
    current_pass = models.OneToOneField(Pass, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Day(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Studio(models.Model):

    def save(self, *args, **kwargs):
        if self.street and self.postal_code and self.city:

            gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
            geocode_result = gmaps.geocode('{} {}, {}'.format(self.postal_code, self.street, self.city))
            try:
                location = geocode_result[0]['geometry']['location']
                self.lat = location.get('lat')
                self.lng = location.get('lng')
            except (IndexError, KeyError, TypeError):
                pass
        super(Studio, self).save(*args, **kwargs)

    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=6, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    nip = models.PositiveIntegerField(null=True, blank=True)
    regon = models.PositiveIntegerField(null=True, blank=True)
    mail = models.EmailField()
    phone = models.PositiveIntegerField(null=True, blank=True)
    lat = models.CharField(max_length=50, null=True, blank=True)
    lng = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name















