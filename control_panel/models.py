from datetime import date
from django.db import models

TYPE_OF_STATUS = ((1, 'Aktywny'), (2, 'Nieaktywny'))
GENDER = ((1, 'Kobieta'), (2, 'Mężczyzna'))
TYPE_OF_LEVEL = ((1, 'Podstawowa'), (2, 'Średnio-zaawansowana'), (3, 'Zaawansowana'))
TYPE_OF_PAYMENT = ((1, 'Opłacony'), (2, 'Do zapłaty'))
TYPE_OF_ACTIVITY = ((1, 'Jumping'), (2, 'Pole Dance'), (3, 'Stretching'))


class Member(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField(null=True)
    gender = models.SmallIntegerField(choices=GENDER, default=1)
    phone = models.IntegerField()
    mail = models.EmailField(unique=True)
    status = models.SmallIntegerField(choices=TYPE_OF_STATUS, default=2)
    notes = models.TextField(null=True)
    img = models.ImageField(upload_to='user_img/', default='user_img/default.jpg')

    def __str__(self):
        self.name = self.first_name + ' ' + self.last_name
        return self.name


class Trainer(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Imię')
    last_name = models.CharField(max_length=64, verbose_name='Nazwisko')
    phone = models.IntegerField(verbose_name='Numer tel.')
    mail = models.EmailField(unique=True, null=True, verbose_name='E-mail')

    def __str__(self):
        self.name = self.first_name + ' ' + self.last_name
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=64, verbose_name='Nazwa')
    validity = models.SmallIntegerField(default=30, verbose_name='Termin ważności')
    available_entries = models.SmallIntegerField(verbose_name='Liczba wejść')
    activity = models.SmallIntegerField(choices=TYPE_OF_ACTIVITY, verbose_name='Rodzaj zajęć', default=2)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Cena')

    def __str__(self):
        return self.name


class Pass(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='passes', verbose_name='Użytkownik')
    product = models.ForeignKey(Product, on_delete=None, verbose_name='Karnet')
    status = models.SmallIntegerField(choices=TYPE_OF_PAYMENT, default=2, verbose_name='Status')
    start_date = models.DateField(default=date.today, verbose_name='Data rozpoczęcia')
    end_date = models.DateField(verbose_name='Data zakończenia')
    entries = models.SmallIntegerField(default=0)


class Group(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa')
    level = models.SmallIntegerField(choices=TYPE_OF_LEVEL, verbose_name='Poziom', default=1)
    program = models.IntegerField(choices=TYPE_OF_ACTIVITY, verbose_name='Rodzaj zajęć')
    trainer = models.ForeignKey(Trainer, models.SET_NULL, null=True, blank=True, related_name='groups',
                                verbose_name='Instruktor')
    members = models.ManyToManyField(Member, verbose_name='Członkowie grupy')


class Entry(models.Model):
    current_pass = models.ForeignKey(Pass, on_delete=models.CASCADE)
    date = models.DateField()
