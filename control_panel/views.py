from datetime import timedelta, date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from .models import Member, Group, Trainer, Pass, Product, Entry
from .forms import LoginForm, EditUserForm, MemberForm, TrainerForm, ProductForm, PassForm, UpdatePassForm, GroupForm,\
    GroupAddMembersForm


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, template_name='control_panel/login.html', context={'form': form})

    def post(self, request):

        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_search = User.objects.filter(email=email)
            if user_search:
                username = user_search[0].username
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))

        form.add_error('email', 'Błędny adres email lub hasło. Spróbuj jeszcze raz')
        return render(request, template_name='control_panel/login.html', context={'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/login')


class LoginAsAnonymous(View):

    def get(self, request):
        user = authenticate(username='tester', password='!Qazxsw2')
        login(request, user)
        return HttpResponseRedirect(reverse('home'))


class EditUserView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = EditUserForm(instance=user)
        return render(request, template_name='control_panel/edit_user.html', context={'form': form})

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = EditUserForm(request.POST, instance=user)
        if user.username == 'tester':
            form.add_error('first_name', 'Tester nie może zmienić użytkownika')
            return render(request, template_name='control_panel/edit_user.html', context={'form': form})

        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))

        return render(request, template_name='control_panel/edit_user.html', context={'form': form})


class HomeView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, template_name='control_panel/main.html', context={})


class ShowMembersView(LoginRequiredMixin, View):

    def get(self, request):
        search = request.GET.get('search')
        members = Member.objects.all().order_by('first_name')

        if search:
            members = Member.objects.filter(Q(first_name__icontains=search) |
                                            Q(last_name__icontains=search) |
                                            Q(mail__icontains=search) |
                                            Q(phone__icontains=search)).order_by('first_name')

        return render(request, template_name='control_panel/member/show_members.html', context={'members': members,
                                                                                                'search': search})


class ShowMemberView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        passes = member.passes.all().order_by('-end_date')
        groups = Group.objects.exclude(members=member)
        return render(request, template_name='control_panel/member/show_member.html',
                      context={'member': member, 'passes': passes, 'groups': groups})


class CreateMemberView(LoginRequiredMixin, CreateView):

    form_class = MemberForm
    template_name = './control_panel/member/member_form.html'
    success_url = reverse_lazy('show_members')


class UpdateMemberView(LoginRequiredMixin, UpdateView):

    form_class = MemberForm
    template_name = './control_panel/member/member_update_form.html'
    model = Member

    def form_valid(self, form):
        instance = form.save(commit=False)
        self.member_id = instance.id
        instance.save()

        return redirect(self.get_success_url(member_id=self.member_id))

    def get_success_url(self, **kwargs):
        member = Member.objects.get(pk=self.kwargs.get('pk'))
        if kwargs is not None:
            return reverse_lazy('show_member', kwargs={'pk': member.id})


class DeleteMemberView(LoginRequiredMixin, DeleteView):

    model = Member
    template_name = './control_panel/member/member_confirm_delete.html'
    success_url = reverse_lazy('show_members')


class ShowTrainersView(LoginRequiredMixin, View):

    def get(self, request):
        search = request.GET.get('search')
        trainers = Trainer.objects.all().order_by('last_name')

        if search:
            trainers = Trainer.objects.filter(Q(first_name__icontains=search) |
                                              Q(last_name__icontains=search) |
                                              Q(mail__icontains=search) |
                                              Q(phone__icontains=search)).order_by('first_name')

        return render(request, template_name='control_panel/trainer/show_trainers.html', context={'trainers': trainers,
                                                                                                  'search': search})


class CreateTrainerView(LoginRequiredMixin, CreateView):

    form_class = TrainerForm
    template_name = './control_panel/trainer/trainer_form.html'
    success_url = reverse_lazy('show_trainers')


class UpdateTrainerView(LoginRequiredMixin, UpdateView):

    form_class = TrainerForm
    template_name = './control_panel/trainer/trainer_update_form.html'
    model = Trainer
    success_url = reverse_lazy('show_trainers')


class DeleteTrainerView(LoginRequiredMixin, DeleteView):

    model = Trainer
    template_name = './control_panel/trainer/trainer_confirm_delete.html'
    success_url = reverse_lazy('show_trainers')


class ShowProductsView(LoginRequiredMixin, View):

    def get(self, request):
        search = request.GET.get('search')
        products = Product.objects.all().order_by('-price')

        if search:
            products = Product.objects.filter(Q(name__icontains=search) |
                                              Q(activity__icontains=search)).order_by('price')

        return render(request, template_name='control_panel/product/show_products.html', context={'products': products,
                                                                                                  'search': search})


class CreateProductView(LoginRequiredMixin, CreateView):

    form_class = ProductForm
    template_name = './control_panel/product/product_form.html'
    success_url = reverse_lazy('show_products')


class UpdateProductView(LoginRequiredMixin, UpdateView):

    form_class = ProductForm
    template_name = './control_panel/product/product_update_form.html'
    model = Product
    success_url = reverse_lazy('show_products')


class DeleteProductView(LoginRequiredMixin, DeleteView):

    model = Product
    template_name = './control_panel/product/product_confirm_delete.html'
    success_url = reverse_lazy('show_products')


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
    template_name = './control_panel/pass/pass_form.html'


class UpdatePassView(LoginRequiredMixin, UpdateView):

    form_class = UpdatePassForm
    template_name = './control_panel/pass/pass_update_form.html'
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

        return render(request, template_name='control_panel/pass/pass_confirm_delete.html', context={'message': message})

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


class ShowScheduleView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, template_name='control_panel/schedule.html', context={})


class ShowGroupsView(LoginRequiredMixin, View):

    def get(self, request):
        search = request.GET.get('search')
        groups = Group.objects.all().order_by('name')

        if search:
            groups = Group.objects.filter(Q(name__icontains=search) |
                                          Q(trainer__last_name__icontains=search)).order_by('name')

        return render(request, template_name='control_panel/group/show_groups.html', context={'groups': groups,
                                                                                              'search': search})


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
        return render(request, template_name='control_panel/group/add_members_form.html', context={'form': form})

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        form = GroupAddMembersForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('show_groups')
        return render(request, template_name='control_panel/group/add_members_form.html', context={'form': form})


class CreateGroupView(LoginRequiredMixin, CreateView):

    form_class = GroupForm
    template_name = './control_panel/group/group_form.html'
    success_url = reverse_lazy('show_groups')


class UpdateGroupView(LoginRequiredMixin, UpdateView):

    form_class = GroupForm
    template_name = './control_panel/group/group_update_form.html'
    model = Group
    success_url = reverse_lazy('show_groups')


class DeleteGroupView(LoginRequiredMixin, DeleteView):

    model = Group
    template_name = './control_panel/group/group_confirm_delete.html'
    success_url = reverse_lazy('show_groups')


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

        return render(request, template_name='control_panel/finances/show_payments.html',
                      context={'passes': passes,
                               'search': search,
                               'start_time': start_time,
                               'end_time': end_time,
                               'user_status': user_status,
                               'pass_status': pass_status
                               })
