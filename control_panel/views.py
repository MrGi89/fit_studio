import json
from datetime import timedelta, date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from .models import Entry, Group, Member, Pass, Product, Trainer, Studio
from .forms import LoginForm, UserForm, MemberForm, TrainerForm, ProductForm, PassForm, GroupForm, StudioForm

# TODO search_query for choseField


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request,
                      template_name='control_panel/login.html',
                      context={'form': form})

    def post(self, request):

        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.get(email=email)
            if user:
                username = user.username
                logged_user = authenticate(username=username, password=password)
                if logged_user is not None:
                    login(request, logged_user)
                    return HttpResponseRedirect(reverse('members'))

        form.add_error('email', 'E-mail address or password is incorrect. Try again.')
        return render(request,
                      template_name='control_panel/login.html',
                      context={'form': form})


class LoginAsAnonymous(View):

    def get(self, request):
        user = authenticate(username='anonymous', password='!Qazxsw2')
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('members'))
        return HttpResponseRedirect(reverse('login'))


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class CreateObjectView(LoginRequiredMixin, View):

    def post(self, request, obj_name):

        if obj_name == 'member':
            form = MemberForm(data=request.POST)
        elif obj_name == 'trainer':
            form = TrainerForm(data=request.POST)
        elif obj_name == 'group':
            form = GroupForm(data=request.POST)
        elif obj_name == 'product':
            form = ProductForm(data=request.POST)
        elif obj_name == 'pass':
            form = PassForm(data=request.POST)
        else:
            raise Http404

        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'result': True}))
        form.errors.update({'result': False})
        return HttpResponse(json.dumps(form.errors))


class UpdateObjectView(LoginRequiredMixin, View):

    def post(self, request, obj_name, pk):

        if obj_name == 'member':
            member = get_object_or_404(Member, pk=pk)
            form = MemberForm(instance=member, data=request.POST)
        elif obj_name == 'trainer':
            trainer = get_object_or_404(Trainer, pk=pk)
            form = TrainerForm(instance=trainer, data=request.POST)
        elif obj_name == 'group':
            group = get_object_or_404(Group, pk=pk)
            form = GroupForm(instance=group, data=request.POST)
        elif obj_name == 'product':
            product = get_object_or_404(Product, pk=pk)
            form = ProductForm(instance=product, data=request.POST)
        elif obj_name == 'user':
            user = get_object_or_404(User, pk=pk)
            form = UserForm(instance=user, data=request.POST)
            if user.username == 'anonymous':
                for field_name in form.changed_data:
                    form.add_error(field_name, 'No permission to change this user\'s data')
        elif obj_name == 'studio':
            studio = Studio.objects.filter(pk=pk)
            if studio:
                form = StudioForm(instance=studio[0], data=request.POST)
            else:
                form = StudioForm(data=request.POST)
        else:
            raise Http404

        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'result': True}))
        form.errors.update({'result': False})
        return HttpResponse(json.dumps(form.errors))


class DeleteObjectView(LoginRequiredMixin, View):

    def get(self, request, redirect_to, pk):

        if redirect_to == 'members':
            member = get_object_or_404(Member, pk=pk)
            member.delete()
        elif redirect_to == 'trainers':
            trainer = get_object_or_404(Trainer, pk=pk)
            trainer.delete()
        elif redirect_to == 'groups':
            group = get_object_or_404(Group, pk=pk)
            group.delete()
        elif redirect_to == 'products':
            product = get_object_or_404(Product, pk=pk)
            product.delete()
        elif redirect_to == 'pass':
            one_pass = get_object_or_404(Pass, pk=pk)
            one_pass.delete()
            return redirect('member', one_pass.member.pk)
        else:
            raise Http404

        return redirect(redirect_to)


class MembersView(LoginRequiredMixin, View):

    def get(self, request):


        page = request.GET.get('page', 1)
        search_query = request.GET.get('search_query')

        if search_query:
            members = Member.objects.filter(Q(first_name__icontains=search_query) |
                                            Q(last_name__icontains=search_query) |
                                            Q(mail__icontains=search_query)).order_by('last_name')
        else:
            members = Member.objects.all().order_by('last_name')

        paginator = Paginator(members, 10)

        return render(request,
                      template_name='control_panel/members.html',
                      context={'members': paginator.get_page(page),
                               'search_query': search_query})


class MemberView(LoginRequiredMixin, View):

    def get(self, request, pk):
        try:
            member = Member.objects.prefetch_related('group_set').get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        # member = get_object_or_404(Member, pk=pk)

        # entries_count = sum([one_pass.entries.all().count() for one_pass in member.passes.all().select_related('entries')])
        # payment_count = sum([one_pass.payment.amount for one_pass in member.passes.all()])
        entries_count = 0
        payment_count = 0
        passes = Pass.objects.select_related('product', 'product__activity').prefetch_related('entries').filter(member=member)
        groups = member.group_set.prefetch_related('days').select_related('activity').all()

        pass_forms = dict()
        warning = False
        for one_pass in passes:
            pass_forms[one_pass.pk] = PassForm(instance=one_pass)
            if not one_pass.paid:
                warning = True
        return render(request,
                      template_name='control_panel/member.html',
                      context={'member': member,
                               'passes': passes,
                               'groups': groups,
                               'form': MemberForm(instance=member),
                               'warning': warning,
                               'pass_form': PassForm(),
                               'pass_forms': pass_forms,
                               'entries_count': entries_count,
                               'payments_count': payment_count})


class TrainersView(LoginRequiredMixin, View):

    def get(self, request):

        page = request.GET.get('page', 1)
        search_query = request.GET.get('search_query')
        if search_query:
            trainers = Trainer.objects.filter(Q(first_name__icontains=search_query) |
                                              Q(last_name__icontains=search_query) |
                                              Q(mail__icontains=search_query)).order_by('last_name')
        else:
            trainers = Trainer.objects.all().order_by('last_name')

        paginator = Paginator(trainers, 10)

        return render(request,
                      template_name='control_panel/trainers.html',
                      context={'trainers': paginator.get_page(page),
                               'search_query': search_query})


class TrainerView(LoginRequiredMixin, View):

    def get(self, request, pk):
        trainer = get_object_or_404(Trainer, pk=pk)
        form = TrainerForm(instance=trainer)
        students = sum([group.members.all().count() for group in trainer.groups.all()])
        week_classes = sum([group.days.all().count() for group in trainer.groups.all()])

        return render(request,
                      template_name='control_panel/trainer.html',
                      context={'trainer': trainer,
                               'students': students,
                               'week_classes': week_classes,
                               'form': form})


class GroupsView(LoginRequiredMixin, View):

    def get(self, request):

        page = request.GET.get('page', 1)
        search_query = request.GET.get('search_query')
        if search_query:
            groups = Group.objects.filter(Q(activity__name__icontains=search_query) |
                                          Q(trainer__first_name__icontains=search_query) |
                                          Q(trainer__last_name__icontains=search_query)).order_by('activity__name', 'level')
        else:
            groups = Group.objects.all().order_by('activity__name', 'level')

        paginator = Paginator(groups, 10)

        return render(request,
                      template_name='control_panel/groups.html',
                      context={'groups': paginator.get_page(page),
                               'search_query': search_query})


class GroupView(LoginRequiredMixin, View):

    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        form = GroupForm(instance=group)
        return render(request,
                      template_name='control_panel/group.html',
                      context={'group': group,
                               'form': form})


class ProductsView(LoginRequiredMixin, View):

    def get(self, request):

        search_query = request.GET.get('search_query')
        if search_query:
            products = Product.objects.filter(Q(type__icontains=search_query)).order_by('-price')
        else:
            products = Product.objects.all().order_by('-price')

        forms = dict()
        for product in products:
            forms[product.pk] = ProductForm(instance=product)

        paginator = Paginator(products, 10)
        page = request.GET.get('page', 1)

        return render(request,
                      template_name='control_panel/products.html',
                      context={'products': paginator.get_page(page),
                               'forms': forms,
                               'search_query': search_query})


class MapView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request,
                      template_name='control_panel/map.html')


class CalendarView(LoginRequiredMixin, View):

    def get(self, request):

        calendar = dict()
        for hour in sorted(Group.objects.values_list('class_time', flat=True)):
            calendar[hour] = {'Monday': list(),
                              'Tuesday': list(),
                              'Wednesday': list(),
                              'Thursday': list(),
                              'Friday': list(),
                              'Saturday': list(),
                              'Sunday': list()}
        for group in Group.objects.prefetch_related('days'):
            for day in group.days.all():
                calendar[group.class_time][day.name].append(group)
        return render(request,
                      template_name='control_panel/calendar.html',
                      context={'calendar': calendar})


class SettingsView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        studio = Studio.objects.filter(pk=1)
        return render(request,
                      template_name='control_panel/settings.html',
                      context={'user_form': UserForm(instance=user),
                               'studio_form': StudioForm(instance=studio[0]) if studio else StudioForm(),

                               })

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = UserForm(request.POST, instance=user)
        if user.username == 'tester':
            form.add_error('first_name', 'Tester nie może zmienić użytkownika')
            return render(request, template_name='control_panel/settings.html', context={'form': form})

        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))

        return render(request, template_name='control_panel/settings.html', context={'form': form})


class GetLocationView(LoginRequiredMixin, View):

    def get(self, request):

        studio = get_object_or_404(Studio, pk=1)
        if studio.lat is None or studio.lng is None:
            raise Http404
        return HttpResponse(json.dumps({'location': {'lat': studio.lat, 'lng': studio.lng}}))










# class CreatePassView(LoginRequiredMixin, CreateView):
#
#     def dispatch(self, request, *args, **kwargs):
#         self.member_id = kwargs.pop('member_id')
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         member = Member.objects.get(id=self.member_id)
#         instance.member = member
#         instance.end_date = instance.start_date + timedelta(days=instance.product.validity)
#         instance.save()
#
#         return redirect(self.get_success_url())
#
#     def get_success_url(self):
#         return '/show_member/{}/'.format(self.member_id)
#
#     form_class = PassForm
#     template_name = './control_panel/old/pass/pass_form.html'
#
#
# class UpdatePassView(LoginRequiredMixin, UpdateView):
#     form_class = UpdatePassForm
#     template_name = './control_panel/old/pass/pass_update_form.html'
#     model = Pass
#
#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         self.pass_id = instance.id
#         instance.save()
#
#         return redirect(self.get_success_url(pass_id=self.pass_id))
#
#     def get_success_url(self, **kwargs):
#         member = Pass.objects.get(pk=self.kwargs.get('pk')).member
#         if kwargs is not None:
#             return reverse_lazy('show_member', kwargs={'pk': member.id})
#
#
# class DeletePassView(LoginRequiredMixin, View):
#
#     def get(self, request, pk):
#
#         current_pass = get_object_or_404(Pass, pk=pk)
#         entries = current_pass.entry_set.all()
#         message = []
#
#         if current_pass.status == 1:
#             message.append('karnet został opłacony')
#         if entries:
#             message.append('karnet został częściowo wykorzystany')
#
#         return render(request, template_name='control_panel/old/pass/pass_confirm_delete.html',
#                       context={'message': message})
#
#     def post(self, request, pk):
#
#         current_pass = get_object_or_404(Pass, pk=pk)
#         user = current_pass.member
#         current_pass.delete()
#         return redirect('/show_member/{}'.format(user.id))
#
#
# class AddPassEntryView(LoginRequiredMixin, View):
#
#     def get(self, request, pk):
#         user_pass = get_object_or_404(Pass, pk=pk)
#
#         if user_pass.entries == user_pass.product.available_entries:
#             new_pass = Pass.objects.create(member=user_pass.member, product=user_pass.product,
#                                            end_date=date.today() + timedelta(days=user_pass.product.validity))
#             new_pass.entries = new_pass.entries + 1
#             new_pass.save()
#             Entry.objects.create(current_pass=new_pass, date=date.today())
#             return redirect('/show_member/{}'.format(user_pass.member.id))
#
#         if user_pass.entries == 0:
#             user_pass.start_date = date.today()
#             user_pass.end_date = date.today() + timedelta(days=user_pass.product.validity)
#
#         user_pass.entries = user_pass.entries + 1
#         Entry.objects.create(current_pass=user_pass, date=date.today())
#         if user_pass.entries == user_pass.product.available_entries:
#             user_pass.end_date = date.today()
#         user_pass.save()
#
#         return redirect('/show_member/{}'.format(user_pass.member.id))
#
#
# class DeletePassEntryView(LoginRequiredMixin, View):
#
#     def get(self, request, pk):
#         entry = get_object_or_404(Entry, pk=pk)
#         current_pass = entry.current_pass
#         current_pass.entries = current_pass.entries - 1
#         current_pass.save()
#         entry.delete()
#         return redirect('/show_member/{}'.format(current_pass.member.id))
#
#
# class UpdatePassStatusView(LoginRequiredMixin, View):
#
#     def get(self, request, pk):
#         user_pass = get_object_or_404(Pass, pk=pk)
#         user_pass.member.status = 1
#         user_pass.member.save()
#
#         if user_pass.status == 2:
#             user_pass.status = 1
#         else:
#             user_pass.status = 2
#         user_pass.save()
#         return redirect('/show_member/{}'.format(user_pass.member.id))
#
#
# class DeleteGroupMemberView(LoginRequiredMixin, View):
#
#     def get(self, request, group_id, member_id, next):
#         member = get_object_or_404(Member, id=member_id)
#         group = get_object_or_404(Group, id=group_id)
#         group.members.remove(member)
#         if next == '0':
#             return redirect('show_groups')
#         return redirect('show_member', member.id)
#
#
# class AddGroupMemberView(LoginRequiredMixin, View):
#
#     def get(self, request, group_id, member_id):
#         member = get_object_or_404(Member, id=member_id)
#         group = get_object_or_404(Group, id=group_id)
#         group.members.add(member)
#         return redirect('show_member', member.id)
