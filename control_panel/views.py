from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from .models import Member, Class, Trainer, Pass
from .forms import LoginForm, EditUserForm, MemberForm, TrainerForm


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


class EditUserView(View):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = EditUserForm(instance=user)
        return render(request, template_name='control_panel/edit_user.html', context={'form': form})

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))

        return render(request, template_name='control_panel/edit_user.html', context={'form': form})


class HomeView(View):

    def get(self, request):
        return render(request, template_name='control_panel/main.html', context={})


class ShowMembersView(View):

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


class ShowMemberView(View):

    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        return render(request, template_name='control_panel/member/show_member.html', context={'member': member})


class CreateMemberView(CreateView):

    form_class = MemberForm
    template_name = './control_panel/member/member_form.html'
    success_url = reverse_lazy('show_members')


class UpdateMemberView(UpdateView):

    form_class = MemberForm
    template_name = './control_panel/member/member_update_form.html'
    model = Member
    success_url = reverse_lazy('show_members')


class DeleteMemberView(DeleteView):
    model = Member
    template_name = './control_panel/member/member_confirm_delete.html'
    success_url = reverse_lazy('show_members')


class ShowTrainersView(View):

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


class CreateTrainerView(CreateView):
    form_class = TrainerForm
    template_name = './control_panel/trainer/trainer_form.html'
    success_url = reverse_lazy('show_trainers')


class UpdateTrainerView(UpdateView):

    form_class = TrainerForm
    template_name = './control_panel/trainer/trainer_update_form.html'
    model = Trainer
    success_url = reverse_lazy('show_trainers')


class DeleteTrainerView(DeleteView):
    model = Trainer
    template_name = './control_panel/trainer/trainer_confirm_delete.html'
    success_url = reverse_lazy('show_trainers')


