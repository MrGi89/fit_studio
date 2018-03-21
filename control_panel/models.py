from django.db import models


TYPE_OF_PASS = ((1, 'Karnet: 4 wejścia'), (2, 'Karnet: 8 wejść'), (3, 'Karnet: 12 wejść'), (4, 'Open'),
                (5, 'FitProfit'), (6, 'Multisport'), (7, 'Multisport + 80'))
TYPE_OF_PRICE = ((1, '140'), (2, '245'), (3, '315'), (4, '350'), (5, '80'), (6, '0'))
TYPE_OF_STATUS = ((1, 'active'), (2, 'not active'))
TYPE_OF_PAYMENT = ((1, 'paid'), (2, 'not paid'))
TYPE_OF_ACTIVITY = ((1, 'Jumping'), (2, 'Pole Dance'), (3, 'Stretching'))


class Member(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Imię')
    last_name = models.CharField(max_length=64, verbose_name='Nazwisko')
    phone = models.IntegerField(verbose_name='Numer tel.')
    mail = models.EmailField(unique=True, verbose_name='E-mail')
    status = models.SmallIntegerField(choices=TYPE_OF_STATUS, default=2, verbose_name='Status')
    description = models.TextField(null=True, verbose_name='Notatka')


class Trainer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.IntegerField()
    mail = models.EmailField(unique=True, null=True)
    

class Pass(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='passes')
    type = models.SmallIntegerField(choices=TYPE_OF_PASS)
    price = models.IntegerField(null=False)
    status = models.SmallIntegerField(choices=TYPE_OF_PAYMENT, default=2)
    entries = models.SmallIntegerField(default=0)


class Class(models.Model):
    level = models.TextField()
    program = models.IntegerField(choices=TYPE_OF_ACTIVITY)
    trainer = models.ForeignKey(Trainer, on_delete=None, related_name='classes')
    members = models.ManyToManyField(Member)
