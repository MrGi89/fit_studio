from datetime import date, timedelta

from django.core.management.base import BaseCommand

from control_panel.models import Member, Pass


class Command(BaseCommand):

# Generates new pass if it ends today. If user didn't used his last pass and didn't pay for it then
# deletes last pass and changes status of user to unactive

    def handle(self, *args, **options):
        members = Member.objects.filter(status=1)

        for member in members:
            last_pass = member.passes.last()

            if last_pass:

                if last_pass.end_date == date.today() and last_pass.status == 2 and last_pass.entries == 0:
                    member.status = 2
                    member.save()
                    last_pass.delete()

                if last_pass.end_date == date.today():
                    Pass.objects.create(member=member,
                                        product=last_pass.product,
                                        start_date=date.today(),
                                        end_date=date.today() + timedelta(days=last_pass.product.validity))
            else:
                member.status = 2
                member.save()
