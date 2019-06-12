import json
from datetime import timedelta, date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from .models import Activity, Entry, Group, Member, Pass, Product, Trainer
from .forms import ActivityForm, LoginForm, EditUserForm, MemberForm, TrainerForm, ProductForm, PassForm, \
    UpdatePassForm, GroupForm, \
    GroupAddMembersForm


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
        elif obj_name == 'activity':
            form = ActivityForm(data=request.POST)
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
        elif obj_name == 'activity':
            activity = get_object_or_404(Activity, pk=pk)
            form = ActivityForm(instance=activity, data=request.POST)
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
        elif redirect_to == 'activities':
            activity = get_object_or_404(Activity, pk=pk)
            activity.delete()
        else:
            raise Http404

        return redirect(redirect_to)


class MembersView(LoginRequiredMixin, View):

    def get(self, request):

        search_query = request.GET.get('search_query')
        if search_query:
            members = Member.objects.filter(Q(first_name__icontains=search_query) |
                                            Q(last_name__icontains=search_query) |
                                            Q(mail__icontains=search_query)).order_by('last_name')
        else:
            members = Member.objects.all().order_by('last_name')
        return render(request,
                      template_name='control_panel/members.html',
                      context={'members': members,
                               'search_query': search_query})


class MemberView(LoginRequiredMixin, View):

    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        form = MemberForm(instance=member)
        entries_count = sum([one_pass.entries.all().count() for one_pass in member.passes.all()])
        payment_count = sum([one_pass.payment.amount for one_pass in member.passes.all()])
        return render(request,
                      template_name='control_panel/member.html',
                      context={'member': member,
                               'form': form,
                               'entries_count': entries_count,
                               'payments_count': payment_count})


class TrainersView(LoginRequiredMixin, View):

    def get(self, request):
        search_query = request.GET.get('search_query')
        if search_query:
            trainers = Trainer.objects.filter(Q(first_name__icontains=search_query) |
                                              Q(last_name__icontains=search_query) |
                                              Q(mail__icontains=search_query)).order_by('last_name')
        else:
            trainers = Trainer.objects.all().order_by('last_name')
        return render(request,
                      template_name='control_panel/trainers.html',
                      context={'trainers': trainers,
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

        search_query = request.GET.get('search_query')
        if search_query:
            groups = Group.objects.filter(Q(activity__name__icontains=search_query) |
                                          Q(trainer__first_name__icontains=search_query) |
                                          Q(trainer__last_name__icontains=search_query))
        else:
            groups = Group.objects.all()
        return render(request,
                      template_name='control_panel/groups.html',
                      context={'groups': groups})


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
            products = Product.objects.filter(Q(name__icontains=search_query)).order_by('-price')
        else:
            products = Product.objects.all().order_by('-price')
        return render(request,
                      template_name='control_panel/products.html',
                      context={'products': products,
                               'search_query': search_query})


class ProductView(LoginRequiredMixin, View):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request,
                      template_name='control_panel/product.html',
                      context={'product': product,
                               'form': form})


class ActivitiesView(LoginRequiredMixin, View):

    def get(self, request):

        search_query = request.GET.get('search_query')
        if search_query:
            activities = Activity.objects.filter(Q(name__icontains=search_query)).order_by('name')
        else:
            activities = Activity.objects.all().order_by('name')
        return render(request,
                      template_name='control_panel/activities.html',
                      context={'activities': activities,
                               'search_query': search_query})


class ActivityView(LoginRequiredMixin, View):

    def get(self, request, pk):

        activity = get_object_or_404(Activity, pk=pk)
        form = ActivityForm(instance=activity)
        return render(request,
                      template_name='control_panel/add/activity.html',
                      context={'activity': activity,
                               'form': form})


class MapView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request,
                      template_name='control_panel/map.html')









class CreatePassView(LoginRequiredMixin, CreateView):

    def dispatch(self, request, *args, **kwargs):
        self.member_id = kwargs.pop('member_id')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        member = Member.objects.get(id=self.member_id)
        instance.member = member
        instance.end_date = instance.start_date + timedelta(days=instance.product.validity)
        instance.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return '/show_member/{}/'.format(self.member_id)

    form_class = PassForm
    template_name = './control_panel/old/pass/pass_form.html'


class UpdatePassView(LoginRequiredMixin, UpdateView):
    form_class = UpdatePassForm
    template_name = './control_panel/old/pass/pass_update_form.html'
    model = Pass

    def form_valid(self, form):
        instance = form.save(commit=False)
        self.pass_id = instance.id
        instance.save()

        return redirect(self.get_success_url(pass_id=self.pass_id))

    def get_success_url(self, **kwargs):
        member = Pass.objects.get(pk=self.kwargs.get('pk')).member
        if kwargs is not None:
            return reverse_lazy('show_member', kwargs={'pk': member.id})


class DeletePassView(LoginRequiredMixin, View):

    def get(self, request, pk):

        current_pass = get_object_or_404(Pass, pk=pk)
        entries = current_pass.entry_set.all()
        message = []

        if current_pass.status == 1:
            message.append('karnet został opłacony')
        if entries:
            message.append('karnet został częściowo wykorzystany')

        return render(request, template_name='control_panel/old/pass/pass_confirm_delete.html',
                      context={'message': message})

    def post(self, request, pk):

        current_pass = get_object_or_404(Pass, pk=pk)
        user = current_pass.member
        current_pass.delete()
        return redirect('/show_member/{}'.format(user.id))


class AddPassEntryView(LoginRequiredMixin, View):

    def get(self, request, pk):
        user_pass = get_object_or_404(Pass, pk=pk)

        if user_pass.entries == user_pass.product.available_entries:
            new_pass = Pass.objects.create(member=user_pass.member, product=user_pass.product,
                                           end_date=date.today() + timedelta(days=user_pass.product.validity))
            new_pass.entries = new_pass.entries + 1
            new_pass.save()
            Entry.objects.create(current_pass=new_pass, date=date.today())
            return redirect('/show_member/{}'.format(user_pass.member.id))

        if user_pass.entries == 0:
            user_pass.start_date = date.today()
            user_pass.end_date = date.today() + timedelta(days=user_pass.product.validity)

        user_pass.entries = user_pass.entries + 1
        Entry.objects.create(current_pass=user_pass, date=date.today())
        if user_pass.entries == user_pass.product.available_entries:
            user_pass.end_date = date.today()
        user_pass.save()

        return redirect('/show_member/{}'.format(user_pass.member.id))


class DeletePassEntryView(LoginRequiredMixin, View):

    def get(self, request, pk):
        entry = get_object_or_404(Entry, pk=pk)
        current_pass = entry.current_pass
        current_pass.entries = current_pass.entries - 1
        current_pass.save()
        entry.delete()
        return redirect('/show_member/{}'.format(current_pass.member.id))


class UpdatePassStatusView(LoginRequiredMixin, View):

    def get(self, request, pk):
        user_pass = get_object_or_404(Pass, pk=pk)
        user_pass.member.status = 1
        user_pass.member.save()

        if user_pass.status == 2:
            user_pass.status = 1
        else:
            user_pass.status = 2
        user_pass.save()
        return redirect('/show_member/{}'.format(user_pass.member.id))


class DeleteGroupMemberView(LoginRequiredMixin, View):

    def get(self, request, group_id, member_id, next):
        member = get_object_or_404(Member, id=member_id)
        group = get_object_or_404(Group, id=group_id)
        group.members.remove(member)
        if next == '0':
            return redirect('show_groups')
        return redirect('show_member', member.id)


class AddGroupMemberView(LoginRequiredMixin, View):

    def get(self, request, group_id, member_id):
        member = get_object_or_404(Member, id=member_id)
        group = get_object_or_404(Group, id=group_id)
        group.members.add(member)
        return redirect('show_member', member.id)


class AddGroupMembersView(LoginRequiredMixin, View):

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        form = GroupAddMembersForm(instance=group)
        return render(request, template_name='control_panel/old/group/add_members_form.html', context={'form': form})

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        form = GroupAddMembersForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('show_groups')
        return render(request, template_name='control_panel/old/group/add_members_form.html', context={'form': form})


class ShowPaymentsView(LoginRequiredMixin, View):

    def get(self, request):
        search = request.GET.get('search')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        user_status = request.GET.get('user_status')
        pass_status = request.GET.get('pass_status')
        passes = Pass.objects.all()

        if start_time:
            passes = passes.filter(start_date__gte=start_time)
        if end_time:
            passes = passes.filter(end_date__lte=end_time)
        if pass_status:
            if pass_status == '1':
                passes = passes.filter(status=1)
            elif pass_status == '2':
                passes = passes.filter(status=2)

        if user_status:
            if user_status == '1':
                passes = passes.filter(member__status=1)
            elif user_status == '2':
                passes = passes.filter(member__status=2)

        if search:
            passes = passes.filter(Q(member__first_name__icontains=search) | Q(member__last_name__icontains=search))

        return render(request, template_name='control_panel/old/finances/show_payments.html',
                      context={'passes': passes,
                               'search': search,
                               'start_time': start_time,
                               'end_time': end_time,
                               'user_status': user_status,
                               'pass_status': pass_status
                               })


class UserView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = EditUserForm(instance=user)
        return render(request, template_name='control_panel/user.html', context={'form': form})

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = EditUserForm(request.POST, instance=user)
        if user.username == 'tester':
            form.add_error('first_name', 'Tester nie może zmienić użytkownika')
            return render(request, template_name='control_panel/user.html', context={'form': form})

        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))

        return render(request, template_name='control_panel/user.html', context={'form': form})
