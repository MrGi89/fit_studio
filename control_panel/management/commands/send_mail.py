from datetime import date, timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from control_panel.models import Member


class Command(BaseCommand):

    def handle(self, *args, **options):
        members = Member.objects.filter(status=1)

        for member in members:
            last_pass = member.passes.last()

            if last_pass:

                if last_pass.start_date + timedelta(days=7) == date.today() and last_pass.status == 2:
                    send_mail('Przypomnienie o płatności',
                              '''
                              Drogi Klubowiczu,
        
                              uprzejmie informujemy, iż zbliża się temin wpłaty za Twój karnet na zajęcia w inSpiral.         
                              Będziemy wdzięczni za uregulowanie płatności w studiu inSpiral. 
                                        
                              Z góry dziękujemy 
                                        
                              Pozdrawiamy serdecznie,
                              inSpiral
                              ''',
                              'admin@inspiral.pl',
                              [last_pass.member.mail],
                              fail_silently=False)
