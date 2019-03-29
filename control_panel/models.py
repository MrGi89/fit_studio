from datetime import date, datetime
from django.db import models

GENDER = ((1, 'Kobieta'), (2, 'Mężczyzna'))
TYPE_OF_STATUS = ((1, 'Aktywny'), (2, 'Nieaktywny'))
TYPE_OF_EMPLOYMENT = ((1, 'UoP'), (2, 'UoZ'), (3, 'UoD'), (4, 'B2B'))
TYPE_OF_LEVEL = ((1, 'Podstawowa'), (2, 'Średnio-zaawansowana'), (3, 'Zaawansowana'))
COLORS = ((1, 'green'), (2, 'red'), (3, 'black'), (4, 'yellow'), (5, 'blue'))


class Member(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.SmallIntegerField(choices=GENDER, default=1)
    phone = models.IntegerField(null=True, blank=True)
    mail = models.EmailField(unique=True)
    status = models.SmallIntegerField(choices=TYPE_OF_STATUS, default=1)
    notes = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='user_img/', default='user_img/default.jpg')

    def __str__(self):
        return self.first_name.capitalize() + ' ' + self.last_name.capitalize()


class Trainer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.SmallIntegerField(choices=GENDER, default=1)
    phone = models.IntegerField()
    mail = models.EmailField(unique=True, null=True, blank=True)
    status = models.SmallIntegerField(choices=TYPE_OF_STATUS, default=1)
    notes = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='trainer_img/', default='trainer_img/default.jpg')
    hourly_rate = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    employment_type = models.SmallIntegerField(choices=TYPE_OF_EMPLOYMENT, default=1)

    def __str__(self):
        return '{} {}'.format(self.first_name.capitalize(), self.last_name.capitalize())


class Product(models.Model):
    name = models.CharField(max_length=64)
    validity = models.SmallIntegerField(default=30)
    available_entries = models.SmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{} {}'.format(self.name, self.available_entries)


class Activity(models.Model):
    name = models.CharField(max_length=64)
    level = models.SmallIntegerField(choices=TYPE_OF_LEVEL, default=1)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        initials = [word[0] for word in self.name.split(' ')]
        return '{}-{}'.format(''.join(initials), self.level)


class Group(models.Model):
    color = models.SmallIntegerField(choices=COLORS)
    max_capacity = models.IntegerField()
    activity = models.ForeignKey(Activity, models.CASCADE, related_name='groups')
    trainer = models.ForeignKey(Trainer, models.SET_NULL, null=True, related_name='groups')
    members = models.ManyToManyField(Member)
    days = models.ManyToManyField('Day')
    class_time = models.TimeField()

    def __str__(self):
        days = ' - '.join([day.name[:3] for day in self.days.all()])
        return '{} {} {}'.format(self.activity, days, self.class_time)


class Pass(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='passes')
    product = models.ForeignKey(Product, on_delete=None, related_name='products')
    paid = models.BooleanField(default=0)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()

    def __str__(self):
        return '{} {} - {}'.format(self.product, self.member, self.paid)


class Entry(models.Model):
    date = models.DateField(default=date.today)
    current_pass = models.ForeignKey(Pass, on_delete=models.CASCADE, related_name='entries')

    def __str__(self):
        return str(self.date)


class Payment(models.Model):
    date = models.DateField()
    current_pass = models.OneToOneField(Pass, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment')
    amount = models.DecimalField(decimal_places=2, max_digits=10)


class Day(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
